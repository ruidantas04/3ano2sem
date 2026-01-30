import sys


def cesar(tipo, key, texto):
    resultado = ""
    texto = texto.upper()

    # Verifica se a chave é válida
    if len(key) != 1 or not key.isalpha():
        print("Erro: A chave deve ser uma única letra do alfabeto.")
        sys.exit(1)

    deslocamento = ord(key) - ord('A')

    for char in texto:
        if char.isalpha():
            base = ord('A')
            if tipo == "enc":
                resultado += chr((ord(char) - base + deslocamento) % 26 + base)
            elif tipo == "dec":
                resultado += chr((ord(char) - base - deslocamento) % 26 + base)
        else:
            resultado += char  # Mantém espaços e caracteres especiais

    return resultado  # Retorna em vez de printar


# Verifica se há argumentos suficientes
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso correto: python3 cesar.py <enc/dec> <chave> <mensagem>")
        sys.exit(1)

    tipo = sys.argv[1]
    key = sys.argv[2]
    texto = sys.argv[3]

    resultado = cesar(tipo, key, texto)
    print(resultado)