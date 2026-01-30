import ply.lex as lex

# Token definitions
tokens = ('PROP', 'NEG', 'DIS', 'CON', 'IMP', 'EQUIV', 'LPAREN', 'RPAREN')
literals = "()"  # Literals for parentheses

# Token definitions
def t_PROP(t):
    r'[A-Z]'  # Match a single uppercase letter for propositions (e.g., P, Q, R)
    return t

def t_NEG(t):
    r'~'  # Match negation symbol (~)
    return t

def t_DIS(t):
    r'\|'  # Match disjunction symbol (|)
    return t

def t_CON(t):
    r'&'  # Match conjunction symbol (&)
    return t

def t_IMP(t):
    r'->'  # Match implication symbol (->)
    return t

def t_EQUIV(t):
    r'<->'  # Match equivalence symbol (<->)
    return t

# Token for left parenthesis
def t_LPAREN(t):
    r'\('  # Match left parenthesis '('
    return t

# Token for right parenthesis
def t_RPAREN(t):
    r'\)'  # Match right parenthesis ')'
    return t

# Ignored characters (spaces and tabs)
t_ignore = r' \t'

# Handle newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling for illegal characters
def t_error(t):
    print(f"Caráter ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Create the lexer
lexer = lex.lex()

# Test input
example_input = "P -> (Q & R) | ~S <-> T"

# Tokenizing the input string
lexer.input(example_input)

# Print the tokens
while (tok := lexer.token()):
    print(tok)
