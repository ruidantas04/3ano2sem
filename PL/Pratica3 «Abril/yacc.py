import ply.yacc as yacc
from lexer import tokens
from lexer import lexer  # Import the lexer object

# Define the operator precedence
precedence = (
    ('right', 'NEG'),         
    ('left', 'CON'),         
    ('left', 'DIS'),          
    ('left', 'IMP'),          
    ('left', 'EQUIV'))   

# Rule for negation (NOT)
def p_expressao_neg(p):
    'expressao : NEG expressao'
    p[0] = not p[2]  

# Rule for conjunction (AND)
def p_expressao_con(p):
    'expressao : expressao CON expressao'
    p[0] = p[1] and p[3]

# Rule for disjunction (OR)
def p_expressao_dis(p):
    'expressao : expressao DIS expressao'
    p[0] = p[1] or p[3]

# Rule for implication (->)
def p_expressao_imp(p):
    'expressao : expressao IMP expressao'
    p[0] = not p[1] or p[3]

# Rule for equivalence (<->)
def p_expressao_equiv(p):
    'expressao : expressao EQUIV expressao'
    p[0] = p[1] == p[3]

# Rule for expressions inside parentheses
def p_expressao_pars(p):
    'expressao : LPAREN expressao RPAREN'
    p[0] = p[2]  # Return the value inside the parentheses

# Rule for propositions (P, Q, etc.)
def p_expressao_PROP(p):
    'expressao : PROP'
    p[0] = input(f"Valor da proposição {p[1]}: ") == 'True'
    
# Error handling rule
def p_error(p):
    print("Erro de sintaxe:", p)
    raise SyntaxError(f"Erro de sintaxe: {p}")

# Create the parser
parser = yacc.yacc()

# Read and parse the input
r = input("Digite a expressão: ")
resultado = parser.parse(r, lexer=lexer)
print("Resultado:", resultado)
