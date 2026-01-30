import ply.lex as lex

frase_exemplo="[1,5,palavra,False,3.14,0,fim]"

tokens = ('Num','Words','Separadores','Bool','LPAREN','RPAREN')

def t_Num(t):
    r'\d+(\.?\d+)?'
    return t

def t_Bool(t): 
    r'(True|False)'
    return t

def t_Words(t):
    r'\w+'
    return t

def t_Separadores(t):
    r'[,;:]'
    return t

def t_LPAREN(t):
    r'\['
    return t
def t_RPAREN(t):
    r'\]'
    return t

def t_error(t):
    print("Caracter ilegal: ", t.value[0])
    t.lexer.skip(1)

lexer=lex.lex()
lexer.input(frase_exemplo)
while r := lexer.token():
    print(r)