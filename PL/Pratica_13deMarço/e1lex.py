import ply.lex as lex
frase_exemplo= "Olá, eu sou o Rui."
tokens= ['Words','Signals','Virgulas']


def t_Words(t):
    r'[\w]+'
    return t

def t_Signals(t):
    r'[.!?]'
    return t
def t_Virgulas(t):
    r','
    return t    
def t_error(t):
    print("Caracter ilegal: ", t.value[0])
    t.lexer.skip(1)

def t_space(t):
    r'\s'
    pass
lexer=lex.lex()

lexer.input(frase_exemplo)
while r := lexer.token():
    print(r)