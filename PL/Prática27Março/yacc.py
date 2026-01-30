import ply.yacc as yacc
from lexer import tokens

# Variáveis globais
total_conta = 0.0

# Regras gramaticais
def p_tudo(p):
    '''tudo : tudo encomenda
            | encomenda'''
    pass

def p_encomenda(p):
    'encomenda : Type DP lista_alimentos'
    pass  # Não fazemos nada com a categoria

def p_lista_alimentos(p):
    '''lista_alimentos : lista_alimentos alimento
                       | alimento'''
    pass

def p_alimento(p):
    'alimento : INDICE QP NAME QP PRICE QP QUANTITY PG'
    global total_conta
    preco = float(p[5])       # garante que é float
    quantidade = int(p[7])    # garante que é int
    subtotal = preco * quantidade
    total_conta += subtotal


def p_error(p):
    if p:
        print(f"Erro de sintaxe perto de: {p.value}")
    else:
        print("Erro de sintaxe: fim de ficheiro inesperado.")

# Criar parser
parser = yacc.yacc()

# Ler e processar o ficheiro
with open(r'C:\Users\Utilizador\Desktop\3ano2sem\PL\Prática27Março\ex.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    parser.parse(content)

# Mostrar o total final
print(f"\n💵 Total da conta: {total_conta:.2f}€")
