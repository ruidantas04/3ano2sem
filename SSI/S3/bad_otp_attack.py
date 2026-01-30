import sys


def xor_bytes(data, key):
    """Aplica a operação XOR entre dois conjuntos de bytes."""
    return bytes(a ^ b for a, b in zip(data, key))


def attack(cipher_file, wordlist):
    """Tenta realizar o ataque XOR usando uma lista de palavras-chave."""
    with open(cipher_file, "rb") as f:
        ciphertext = f.read()

    for word in wordlist:
        word_bytes = word.encode()
        key_guess = xor_bytes(ciphertext[:len(word_bytes)], word_bytes)

        # Decifra o texto completo usando a chave adivinhada
        plaintext_guess = xor_bytes(ciphertext, key_guess)

        # Tenta encontrar uma palavra legível no texto decifrado
        try:
            decoded_text = plaintext_guess.decode(errors='ignore')
            # Verifica se alguma das palavras-chave aparece no texto decifrado
            if any(word in decoded_text for word in wordlist):
                print(f"Texto decifrado: {decoded_text}")
                return
        except UnicodeDecodeError:
            pass

    print("Nenhuma correspondência encontrada.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python bad_otp_attack.py <arquivo_cifrado> <palavras-chave>")
        sys.exit(1)

    cipher_file = sys.argv[1]
    wordlist = sys.argv[2:]
    attack(cipher_file, wordlist)
