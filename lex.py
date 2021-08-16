import ply.lex as lex

tokens = (
#    "STR",
    "NUMBER",
    "ID",
    "STR",
    "IF",
    "ELSE",
    "WHILE",
    "PLUS",
    "MINUS",
    "KAKERU",
    "WARU",
    "EQOL",
    "EQOLS",
    "DAINARI",
    "SYOUNARI",
    "CONMA",
    "PIRIOD",
    "KAKKO",
    "KOKKA",
    "LKAKKO",
    "LKOKKA",
    "PUT",
    "COLON",
    "SEMI",
    "END",
    "FN",
    "RETURN",
    "INPUT",
    "INCLUDE",
    "RDM",
    "LEN",
    "BREAK",
    "OPEN",
    "WRITE",
    "CLOSE",
    "STP",
    "CLASS",
    "INST",
    "PASS",
    "TYPE",
    "VOID",
    "ARROW",
    "LOOP",
)

t_CONMA = r","
t_PIRIOD = r"\."
t_PLUS = r"\+"
t_MINUS = r"\-"
t_KAKERU = r"\*"
t_WARU = r"\/"
t_EQOL = r"\="
t_EQOLS = r"\=\="
t_KAKKO = r"\("
t_KOKKA = r"\)"
t_NUMBER = r"\d+"
t_LKAKKO = r"\["
t_LKOKKA = r"\]"
t_ignore = r' \t'
t_COLON = r"\:"
t_SEMI = r"\;"
t_DAINARI = r"\>"
t_SYOUNARI = r"\<"
t_ARROW = r"\-\>"

#t_QOT = r"\""
#t_OR = r"\|\|"
#t_AND = "&&"

def t_STR (t):
    r"[\"'][_\<\>\.,\*+-/\!\?a-zA-Z0-9\"'\\ ]*"
    return t

def t_ID (t):
    r"[@a-zA-Z\_][a-zA-Z0-9_|\&]*"
    if t.value == "int":
        t.type = "TYPE"
    elif t.value == "str":#t.value == "float" or 
        t.type = "TYPE"
    elif t.value == "void":
        t.type = "VOID"
    elif t.value == "put":
        t.type = "PUT"
    elif t.value == "end":
        t.type = "END"
    elif t.value == "if":
        t.type = "IF"
    elif t.value == "else":
        t.type = "ELSE"
    elif t.value == "elif":
        t.type = "ELIF"
    elif t.value == "while":
        t.type = "WHILE"
    elif t.value == "fn":
        t.type = "FN"
    elif t.value == "return":
        t.type = "RETURN"
    elif t.value == ",":
        t.type = "CONMA"
    elif t.value == "input":
        t.type = "INPUT"
    elif t.value == "&&" or t.value == "and":
        t.type = "AND"
    elif t.value == "||" or t.value == "or":
        t.type = "OR"
    elif t.value == "@include":
        t.type = "INCLUDE"
    elif t.value == "rdm":#rdm(seed1, seed2);
        t.type = "RDM"
    elif t.value == "LEN":
        t.type = "LEN"
    elif t.value == "break":
        t.type = "BREAK"
    elif t.value == "open":
        t.type = "OPEN"
    elif t.value == "write":
        t.type = "WRITE"
    elif t.value == "close":
        t.type = "CLOSE"
    elif t.value == "allstop":
        t.type = "STP"
    elif t.value == "class":
        t.type = "CLASS"
    elif t.value == "inst":
        t.type = "INST"
    elif t.value == "pass":
        t.type = "PASS"
    elif t.value == "loop":
        t.type = "LOOP"
    else:
        t.type == "ID"
    return t

def t_error(t):
    print("LexErr：%s, それ、あなたの感想ですよね？" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex(debug=0)
