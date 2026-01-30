import sys
import os

def attack_chacha20(fctxt, pos, ptxtAtPos, newPtxtAtPos):
    """Manipula um criptograma ChaCha20 para alterar um fragmento conhecido."""
    # Lê o criptograma original
    with open(fctxt, 'rb') as input_file:
        data = input_file.read()

    # Define o tamanho do nonce (ajuste conforme a implementação do ChaCha20)
    NONCE_SIZE = 8  # Pode ser 12 em algumas implementações
    if len(data) < NONCE_SIZE:
        print("Erro: O arquivo é muito pequeno para conter um nonce válido.")
        sys.exit(1)

    # Separa o nonce e o criptograma
    nonce = data[:NONCE_SIZE]
    ciphertext = data[NONCE_SIZE:]

    # Converte os parâmetros
    try:
        pos = int(pos)  # Posição como inteiro
    except ValueError:
        print("Erro: A posição deve ser um número inteiro.")
        sys.exit(1)

    ptxtAtPos = ptxtAtPos.encode('utf-8')  # Texto-limpo conhecido como bytes
    newPtxtAtPos = newPtxtAtPos.encode('utf-8')  # Novo texto-limpo como bytes

    # Verifica se os tamanhos de ptxtAtPos e newPtxtAtPos são iguais
    if len(ptxtAtPos) != len(newPtxtAtPos):
        print("Erro: O tamanho de <ptxtAtPos> e <newPtxtAtPos> deve ser igual.")
        sys.exit(1)

    # Verifica se a posição + tamanho cabe no criptograma
    if pos < 0 or pos + len(ptxtAtPos) > len(ciphertext):
        print(f"Erro: A posição {pos} ou o tamanho excedem o criptograma (tamanho: {len(ciphertext)}).")
        sys.exit(1)

    # Converte o criptograma para uma lista de bytes mutável
    ciphertext_bytes = bytearray(ciphertext)

    # Calcula a keystream no trecho conhecido: K = P ⊕ C
    keystream = bytes(a ^ b for a, b in zip(ptxtAtPos, ciphertext[pos:pos + len(ptxtAtPos)]))

    # Calcula o novo criptograma no trecho: C' = P' ⊕ K
    new_ciphertext_chunk = bytes(a ^ b for a, b in zip(newPtxtAtPos, keystream))

    # Substitui o trecho no criptograma original
    ciphertext_bytes[pos:pos + len(newPtxtAtPos)] = new_ciphertext_chunk

    # Salva o criptograma manipulado
    output_file = fctxt + '.attck'
    with open(output_file, 'wb') as output_file:
        output_file.write(nonce + ciphertext_bytes)
    print(f"Criptograma manipulado salvo em {output_file}")

def main():
    # Verifica se os argumentos foram fornecidos corretamente
    if len(sys.argv) != 5:
        print("Uso: python chacha20_int_attck.py <fctxt> <pos> <ptxtAtPos> <newPtxtAtPos>")
        sys.exit(1)

    fctxt = sys.argv[1]
    pos = sys.argv[2]
    ptxtAtPos = sys.argv[3]
    newPtxtAtPos = sys.argv[4]

    # Executa o ataque
    attack_chacha20(fctxt, pos, ptxtAtPos, newPtxtAtPos)

if __name__ == "__main__":
    main()