import ply.yacc as yacc

from calc_lex import tokens

def p_operacao_1(p):
    "operacao : calc "
    p[0] = p[1]

def p_operacao_2(p):
    """operacao : operacao PLUS calc """
    p[0] = p[1] + p[3]

def p_operacao_3(p):
    "operacao : operacao SUB calc"
    p[0] = p[1] - p[3]

def p_calc_1(p):
    "calc : expressao"
    p[0] = p[1] 

def p_calc_2(p):
    "calc : calc TIMES expressao"
    p[0] = p[1] * p[3]

def p_calc_3(p):
    "calc : calc DIV expressao"
    p[0] = p[1] / p[3]

def p_expressao1(p):
    "expressao : NUMBER"
    p[0] = p[1]

def p_expressao(p):
    "expressao : LPAREN operacao RPAREN"
    p[0] = p[2]

def p_error(p):
    print("Erro sintático no input!")
parser = yacc.yacc()
r = parser.parse("(3+2)*3")

print(r)