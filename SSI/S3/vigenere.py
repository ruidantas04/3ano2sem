import sys

# Função para criptografar ou descriptografar com Vigenère
def vigenere(tipo, chave, texto):
    resultado = ""
    chave = chave.upper()
    texto = texto.upper()

    chave_len = len(chave)
    j = 0

    for i in range(len(texto)):
        char = texto[i]
        if char.isalpha():  # Só criptografa letras
            deslocamento = ord(chave[j % chave_len]) - ord('A')  # Pega o valor da chave
            if tipo == "enc":
                resultado += chr((ord(char) - ord('A') + deslocamento) % 26 + ord('A'))  # Criptografia
            elif tipo == "dec":
                resultado += chr((ord(char) - ord('A') - deslocamento) % 26 + ord('A'))  # Descriptografia
            j += 1
        else:
            resultado += char

    return resultado

# Função principal para rodar pelo terminal
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso correto: python3 vigenere.py <enc/dec> <chave> <mensagem>")
        sys.exit(1)

    tipo = sys.argv[1]
    chave = sys.argv[2]
    texto = sys.argv[3]

    resultado = vigenere(tipo, chave, texto)
    print(resultado)
