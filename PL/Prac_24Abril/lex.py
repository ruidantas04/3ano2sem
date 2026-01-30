import ply.lex as lex

# Frase exemplo
frase = """PUSH 1
PUSH 2
OP +

PUSH 5
PUSH 1
OP -

OP *
POP"""

# Lista de tokens
tokens = (
    'PUSH',
    'POP',
    'OP',
    'OPERADOR',
    'NUM',
    'SWAP'
)

# Expressões regulares para os tokens
t_PUSH = r'PUSH'
t_POP = r'POP'
t_OP = r'OP'
t_OPERADOR= r'[\+\-\*\/]'
t_SWAP = r'SWAP'

# Token para números
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Contar novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Caractere inválido '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Construção do lexer
lexer = lex.lex()

# Testar o lexer
def test_lexer(frase):
    lexer.input(frase)
    for tok in lexer:
        print(tok)

# Executar o teste
test_lexer(frase)
