import sys
from cesar import cesar


def cesar_attack(texto, palavras_conhecidas):
    for key in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        tentativa = cesar('dec', key, texto)

        for palavra in palavras_conhecidas:
            if palavra.upper() in tentativa:
                print(f"Chave encontrada: {key}")
                print(f"Texto descriptografado: {tentativa}")
                return key

    print("Nenhuma chave válida encontrada.")
    return None


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso correto: python3 cesar_attack.py <texto> <palavra1> [<palavra2> ...]")
        sys.exit(1)

    texto = sys.argv[1]
    palavras_conhecidas = sys.argv[2:]  # Pode passar várias palavras para verificar

    cesar_attack(texto, palavras_conhecidas)