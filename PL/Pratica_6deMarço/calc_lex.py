import ply.lex as lex

frase_exemplo= """3 * ( 5 + 2 )
               3 * ( 5 + 2)"""

tokens = (
    'NUMBER', # 5
    'ADD',    # +
    'MULT',   # *
    'SUB',    # -
    'LPAREN', # (
    'RPAREN', # )
    'DIV',    # /
)

def t_NUMBER(t) :
    r"\d+"
    t.value = int(t.value)
    return t
    
t_ADD = r"\+"
t_MULT = r"\*"
t_SUB = r"\-"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_DIV = r"/"

def t_error(t):
    print("Caracter ilegal: ", t.value[0])
    t.lexer.skip(1)

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += 1
    


lexer=lex.lex()

