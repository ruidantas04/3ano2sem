import sys
import itertools
from collections import Counter
from vigenere import vigenere
from cesar import cesar

# Ordem de candidatos de letras esperadas (plaintext) para a letra mais frequente
CANDIDATOS_PT = "AEOS"


def divide_texto(text, tam):
    """Divide o texto cifrado em 'tam' grupos, conforme a posição na chave."""
    blocks = ['' for _ in range(tam)]
    for i in range(len(text)):
        blocks[i % tam] += text[i]
    return blocks


def letra_mais_frequente(text):
    """Retorna a letra mais frequente (maior contagem) num bloco de texto."""
    contador = Counter(text)
    if contador:
        return max(contador, key=contador.get)
    return None


def candidatos_para_bloco(bloco):
    """
    Para um bloco de texto cifrado, retorna uma lista de letras candidatas
    para a posição da chave, com base na hipótese de que a letra mais frequente
    do texto limpo é uma das letras em CANDIDATOS_PT.

    Se o bloco tiver como letra mais frequente L, para cada candidato 'p' (por exemplo, 'A'),
    calculamos a chave como: chave = (ord(L) - ord(p)) mod 26.
    """
    L = letra_mais_frequente(bloco)
    candidatos = []
    if L:
        for p in CANDIDATOS_PT:
            shift = (ord(L) - ord(p)) % 26
            candidato_chave = chr(shift + ord('A'))
            candidatos.append(candidato_chave)
    else:
        candidatos.append('A')
    return candidatos


def vigenere_attack(tam, text, words):
    tam = int(tam)
    words = [w.upper() for w in words]  # Converter palavras para maiúsculas
    blocks = divide_texto(text, tam)

    # Para cada bloco, obtemos uma lista de candidatos para a letra da chave
    lista_candidatos = []
    for i, bloco in enumerate(blocks):
        candidatos = candidatos_para_bloco(bloco)
        print(f"Bloco {i + 1}: {bloco} -> Candidatos: {candidatos}")
        lista_candidatos.append(candidatos)

    # Gera todas as combinações possíveis (produto cartesiano)
    for chave_tuple in itertools.product(*lista_candidatos):
        chave_candidata = ''.join(chave_tuple)
        decrypted_text = vigenere('dec', chave_candidata, text)
        # Verifica se alguma palavra conhecida aparece no texto decifrado
        if any(word in decrypted_text for word in words):
            print("\n✅ Chave correta encontrada!")
            print(chave_candidata)
            print(decrypted_text)
            return

    print("\n❌ Nenhuma chave válida encontrada.")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso correto: python3 vigenere_attack.py <tamanho_da_chave> <texto_cifrado> <palavra1> [<palavra2> ...]")
        sys.exit(1)

    tamanho = sys.argv[1]
    texto = sys.argv[2]
    palavras_conhecidas = sys.argv[3:]

    vigenere_attack(tamanho, texto, palavras_conhecidas)
