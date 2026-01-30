import ply.lex as lex

tokens=('Type','DP','QP','INDICE','NAME','PRICE','QUANTITY','PG')


def t_PRICE(t):
    r'\d+\.\d+'
    return t

def t_INDICE(t):
    r'\-\s*\d+'
    t.value = int(t.value.strip()[1:])  
    return t
    
def t_QUANTITY(t):
    r'\d+'
    t.value=int(t.value)
    return t

def t_Type(t):
    r'[A-Z][A-Z]+'
    return t 

def t_NAME(t):
    r'[\S]\w+[ \w]*'
    return t

def t_QP(t):
     r'\:\:'
     return t

def t_DP(t):
     r'\:'
     return t
def t_PG(t):
    r'\;'
    return t
 
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()
with open(r'C:\Users\Utilizador\Desktop\3ano2sem\PL\Prática27Março\ex.txt', 'r', encoding='utf-8') as file:
    for line in file:
        lexer.input(line)
        while tok := lexer.token():
            print(tok)

