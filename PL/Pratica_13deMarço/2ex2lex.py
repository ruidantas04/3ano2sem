import ply.lex as lex

# Definição dos estados (ON/OFF)
states = (
    ('off', 'exclusive'),  # estado exclusivo onde o somador está desligado
)

# Tokens que serão utilizados
tokens = ('ON', 'OFF', 'Num', 'EQUAL')

# Inicializamos a soma como 0
soma = 0
estado_somador = True  # O somador começa ligado por padrão

# Definição dos tokens no estado inicial (ON)
def t_ON(t):
    r'on|On|ON'  # aceitamos qualquer combinação de maiúsculas/minúsculas
    t.lexer.begin('INITIAL')  # volta ao estado inicial
    global estado_somador
    estado_somador = True  # liga o somador
    return t

def t_OFF(t):
    r'off|Off|OFF'  # aceitamos qualquer combinação de maiúsculas/minúsculas
    t.lexer.begin('off')  # entra no estado 'off' para desligar o somador
    global estado_somador
    estado_somador = False  # desliga o somador
    return t

def t_Num(t):
    r'\d+'  # números inteiros
    t.value = float(t.value)  # converte o valor para float
    if estado_somador:
        global soma
        soma += t.value  # adiciona o número à soma se o somador estiver ligado
    return t

def t_EQUAL(t):
    r'='  # quando encontrar "=", imprime a soma atual
    print(f"Resultado da soma: {soma}")
    return t

# Funções para lidar com os erros
def t_off_error(t):
    # Caso um token inválido seja encontrado no estado OFF
    print(f"Caracter ilegal no estado OFF: {t.value[0]}")
    t.lexer.skip(1)  # Ignora o token inválido

def t_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    t.lexer.skip(1)  # Ignora o token inválido

# Funções específicas para o estado 'off'
# No estado off, não vamos somar os números, só ignorar os valores.
def t_off_Num(t):
    r'\d+'  # Números que são ignorados no estado 'off'
    t.lexer.skip(len(t.value))  # Ignora o número
    return t

def t_space(t):
    r'\s'  # Ignora espaços no estado inicial
    pass

def t_off_space(t):
    r'\s'  # Ignora espaços no estado 'off'
    pass

# Corrigir a função t_off_equal para retornar o token correto 'EQUAL'
def t_off_EQUAL(t):
    r'='
    print(f"Resultado da soma: {soma}")
    return t

# Criando o analisador léxico
lexer = lex.lex()

# Função para processar a entrada
def process_input(data):
    global soma
    soma = 0  # Reseta a soma a cada nova execução
    lexer.input(data)  # Inicializa a entrada do lexer
    while token := lexer.token():  # Lê todos os tokens até o final
        pass

# Leitura de entrada (pode ser do stdin ou de um arquivo)
if __name__ == "__main__":
    # Lê a entrada do usuário
    data = input("Digite uma expressão com ON/OFF e números (exemplo: 'ON 3 2 ='): ")
    process_input(data)
