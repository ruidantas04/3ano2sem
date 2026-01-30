import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def generate_key(fkey):
    key = os.urandom(32)
    with open(fkey, "wb") as f:
        f.write(key)
    print(f"Chave gerada e guardada em {fkey}")

def encrypt_file(fich, fkey):
    with open(fkey, "rb") as f:
        key = f.read(32)

    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(nonce))
    encryptor = cipher.encryptor()

    with open(fich, "rb") as fin:
        plaintext = fin.read()

    # Aplicar Padding (PKCS7) para garantir que o tamanho seja múltiplo de 16
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    with open(fich + ".enc", "wb") as fout:
        fout.write(nonce + ciphertext)

    print(f"Ficheiro cifrado guardado como {fich}.enc")

def decrypt_file(fich, fkey):
    with open(fkey, "rb") as f:
        key = f.read(32)

    with open(fich, "rb") as fin:
        nonce = fin.read(16)
        ciphertext = fin.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(nonce))
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remover o Padding
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    with open(fich + ".dec", "wb") as fout:
        fout.write(plaintext)

    print(f"Ficheiro decifrado guardado como {fich}.dec")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: cfich_aes_cbc.py <setup|enc|dec> <fich> [<fkey>]")
        sys.exit(1)

    operation = sys.argv[1]

    if operation == "setup":
        fkey = sys.argv[2]
        generate_key(fkey)

    elif operation == "enc":
        if len(sys.argv) < 4:
            print("Uso: cfich_aes_cbc.py enc <fich> <fkey>")
            sys.exit(1)
        encrypt_file(sys.argv[2], sys.argv[3])

    elif operation == "dec":
        if len(sys.argv) < 4:
            print("Uso: cfich_aes_cbc.py dec <fich> <fkey>")
            sys.exit(1)
        decrypt_file(sys.argv[2], sys.argv[3])

    else:
        print("Operação inválida! Use setup, enc ou dec.")
