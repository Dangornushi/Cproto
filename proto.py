import sys, struct
import ply.yacc as yacc
from lex import tokens
import subprocess


def p_sents(p):
    """
    sents : sent
          | sents sent
    """
    if (len(p) > 2):
        l = list([p[1]])
        l.append(p[2])
        p[0] = l
    else:
        p[0] = p[1]

def p_paramlist(p):
    """
    paramlist : TYPE ID
              | VOID
              | paramlist CONMA TYPE ID
    """
    # ! important point!
    if p[1] == "void":
        p[0] = ("void", "None")

    elif (len(p) == 3):
        l = [p[1], p[2]]
        p[0] = l
    else:
        p[0] = p[1],
        if type(p[1][0]) == list:
            l = list(p[1])
        else:
            l = list([p[1]])
        l.append(p[3], p[4])
        p[0] = l
    
def p_args(p):
    """
    args : ID
         | VOID
         | args CONMA ID
    """
    # ! important point!
    if (len(p) == 2):
        l = p[1]
        p[0] = l
    else:
        p[0] = p[1],
        if type(p[1][0]) == list:
            l = list(p[1])
        else:
            l = list(p[1])
        l.append(p[3])
        p[0] = l


def p_sent_shiki(p):
    """
    shiki : ID
          | STR
          | NUMBER
    """
    p[0] = ("shiki", p[1])
def p_shiki_calc(p):
    """
    shiki : shiki PLUS shiki
          | shiki MINUS shiki
          | shiki KAKERU shiki
          | shiki WARU shiki
          | ID LKAKKO shiki LKOKKA 
    """
    if p[2] == "+": 
        p[0] = ("add", p[1], p[2], p[3])
    elif p[2] == "-":
        p[0] = ("sub", p[1], p[2], p[3])
    elif p[2] == "/":
        p[0] = ("mul", p[1], p[2], p[3])
    elif p[2] == "*":
        p[0] = ("div", p[1], p[2], p[3])
    else:
        p[0] = ("char", p[1], p[3])

def p_sent_class(p):
    """
    sent : CLASS ID COLON sents END SEMI 
    """
    p[0] = ("defclass", p[2], p[4])

def p_sent_defunc(p):
    """
    sent : FN ID KAKKO paramlist KOKKA ARROW TYPE COLON sents END SEMI
    """
    p[0] = ("defunc", p[2], p[4], p[7], p[9])

def p_sent_if(p):
    """
    sent : IF compa COLON sents END SEMI
    """
    p[0] = ( "if", p[2], p[4])

def p_sent_ifelse(p):
    """
    sent : IF compa COLON sents ELSE COLON sents END SEMI
    """
    p[0] = ( "if-else", p[2], p[4], p[7])

def p_sent_while(p):
    """
    sent : WHILE compa COLON sents END SEMI
    """
    p[0] = ( "while", p[2], p[4] )

def p_compa(p):
    """
    compa : shiki EQOLS shiki
          | shiki DAINARI shiki
          | shiki SYOUNARI shiki
    """
    p[0] = ("compa", p[1], p[2], p[3] )

def p_compa_call(p):
    """
    compa : ID KAKKO paramlist KOKKA
    """
    p[0] = ("compacall", p[1], p[3])

def p_compa_callvoid(p):
    """
    compa : ID KAKKO KOKKA
    """
    p[0] = ("compacall", p[1], "0")

def p_sent_defvall(p):
    """
    sent : TYPE ID EQOL shiki SEMI
    """
    p[0] = ("mov", p[1], p[2], p[4])

def p_sent_inst(p):
    """
    sent : CLASS ID EQOL AT ID KAKKO args KOKKA SEMI
    """
    p[0] = ( "inst", p[2], p[5], p[7])

def p_sent_pass(p):
    """
    sent : PASS SEMI
    """
    p[0] = ("PASS")

def p_sent_put(p):
    """
    sent : PUT shiki SEMI
    """
    p[0] = ( "put", p[2] )

def p_sent_public(p):
    """
    sent : AT PUB SEMI
    """
    p[0] = "pub"

def p_sent_call(p):
    """
    sent : ID KAKKO args KOKKA SEMI
    """
    p[0] = ( "call", p[1], p[3])

def p_sent_class_call(p):
    """
    sent : ID PIRIOD ID KAKKO args KOKKA SEMI
    """
    p[0] = ( "class_call", p[1], p[3], p[5])

def p_sent_return(p):
    """
    sent : RETURN shiki SEMI
    """
    p[0] = ("ret", p[2])

def p_error(p):
    print( "SyntaxErr : %s" % p )

parser = yacc.yacc(debug=0, write_tables=0)

funcname = ""
nowvall = ""
now = ""

public = False

datalis = []
includes = []

class Walker:
    def __init__(self):
        pass

    def append( self, data ):
        global datalis
        datalis.append(data)
    
    def file_write(self):
        global datalis
        with open(sys.argv[1]+".cpp", "w") as fout:
            for x in datalis:
                fout.write(x)

    def steps(self, ast):
        global funcname, nowvall, now

        arg = ""

        if  ast[0] == "defunc":
            if ast[2][0] == "void":
                pass
            else:
                #TODO : 引数単数と複数の処理 ->　argに格納
                if ast[2][0] == "str":
                    arg = "std::string "+ast[2][1]
            self.append(ast[3] + " " + ast[1] + "(" + arg + ") { " )
            self.steps(ast[4])
            self.append("}\n")
        
        elif ast[0] == "defclass":
            now = ast[1]+"::"
            self.append("class "+ast[1]+" { ")
            self.steps(ast[2])
            self.append("};\n");
            now = ""
        
        elif ast[0] == "pub":
            public = True
            self.append("public: ")
            self.steps(ast[1:])
        
        elif ast[0] == "inst":
            self.append(ast[2]+" "+ast[1]+"; ");

        elif ast[0] == "call":
            self.append(ast[1]+"("+ast[2]+"); ")
        
        elif ast[0] == "class_call":
            if ast[3] == "void":
                self.append(ast[1]+"."+ast[2]+"("+"); ")
            else:
                self.append(ast[1]+"."+ast[2]+"("+ast[3]+"); ")

        elif ast[0] == "if":
            self.steps(ast[1])
            self.append("if "+nowvall+" { ")
            self.steps(ast[2])
            self.append(" } ")

        elif ast[0] == "if-else":
            self.steps(ast[1])
            self.append("if "+nowvall+" { ")
            self.steps(ast[2])
            self.append(" } else { ")
            self.steps(ast[3])
            self.append(" } ")
        
        elif ast[0] == "while":
            self.steps(ast[1])
            self.append("while "+nowvall+" { ")
            self.steps(ast[2])
            self.append(" } ")
        
        elif ast[0] == "compa":
            self.steps(ast[1])
            beforevall = nowvall
            self.steps(ast[3])
            nowvall = "( "+beforevall+" "+ast[2]+" "+nowvall+" )"
        
        elif ast[0] == "mov":
            mode = ""
            if "string.h" in includes:
                pass
            else:
                includes.append("string.h")
                datalis.insert(0, "#include<string>\n")

            self.steps(ast[3])

            if ast[3][0] != "add" and ast[3][0] != "sub" and ast[3][0] != "div" and ast[3][0] != "mul":
                if ast[1] == "str":
                    mode = "std::string "
                elif ast[1] == "int":
                    mode = "int "
            else:
                mode = ""

            self.append(mode+ast[2]+" = "+nowvall+"; ")
        
        elif ast[0] == "char":
            self.steps(ast[2])
            nowvall = ast[1]+"["+nowvall+"]"

        elif ast[0] == "put":
            if "iostream" in includes:
                pass
            else:
                includes.append("iostream")
                datalis.insert(0, "#include<iostream>\n")
            self.steps(ast[1])
            try:
                x = int(nowvall)
                self.append("std::cout << \"%d\", "+nowvall+" << std::endl; ")
            except:
                self.append("std::cout << "+nowvall+" << std::endl; ")
        
        elif ast[0] == "ret":
            self.steps(ast[1])
            self.append("return "+str(nowvall)+"; ")

        elif ast[0] == "shiki":
            nowvall = ast[1]
        
        elif ast[0] == "add":
            self.steps(ast[1])
            beforvall = nowvall;
            self.steps(ast[3])
            try:
                x = int(beforvall)
                try:
                    y = int(nowvall)
                    shiki = str(x+y)
                except:
                    shiki = x+" + "+str(y)
            except:
                shiki = beforvall + "+" + nowvall
            
            nowvall = shiki
        
        elif ast[0] == "sub":
            self.steps(ast[1])
            beforvall = nowvall;
            self.steps(ast[3])
            try:
                x = int(beforvall)
                try:
                    y = int(nowvall)
                    shiki = str(x-y)
                except:
                    shiki = x+" - "+str(y)
            except:
                shiki = beforvall + " - " + nowvall
            
            nowvall = shiki
        
        elif ast[0] == "div":
            self.steps(ast[1])
            beforvall = nowvall;
            self.steps(ast[3])
            try:
                x = int(beforvall)
                try:
                    y = int(nowvall)
                    shiki = str(x*y)
                except:
                    shiki = x+" * "+str(y)
            except:
                shiki = beforvall + "*" + nowvall
            
            nowvall = shiki
        
        elif ast[0] == "mul":
            self.steps(ast[1])
            beforvall = nowvall;
            self.steps(ast[3])
            try:
                x = int(beforvall)
                try:
                    y = int(nowvall)
                    shiki = str(x/y)
                except:
                    shiki = x+" / "+str(y)
            except:
                shiki = beforvall + "/" + nowvall
            
            nowvall = shiki

        elif ast == "PASS":
            pass

    
        elif type(ast[0]) == list or type(ast[0]) == tuple:
            for item in ast:
                self.steps(item) 


if __name__ == "__main__":
    walker = Walker()
    infunc = False
    result = ""

    open_file = open(sys.argv[1], "r", encoding="utf_8").readlines()

    for item in open_file:
            item = item.replace("\n", "")
            if item.startswith("fn ") or item.startswith("if ")  or item.startswith("while ") or item.startswith("class "):
                infunc = True
                result = ""
                result += item
            elif item.startswith("end;"):
                infunc = False
                result += item
                if result != None:
                    walker.steps(parser.parse(result))
            elif infunc and item != "\n":
                result += item
            else:
                if item != None and item != "\n" and item != "":
                    walker.steps(parser.parse(item))
            walker.file_write()
    args = ['g++','-o', sys.argv[1].split(".")[0], sys.argv[1]+".cpp"]
    subprocess.check_output(args)
    if len(sys.argv) > 2:
        if sys.argv[2] == "-ne":
            pass
        else:
            pass
    else:
        args = ["rm",sys.argv[1]+".cpp"]
        subprocess.check_output(args)
