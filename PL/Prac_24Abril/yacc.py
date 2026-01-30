import ply.yacc as yacc
from lex import tokens

# Definição da gramática
def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]
    print("Programa analisado com sucesso!")
    
