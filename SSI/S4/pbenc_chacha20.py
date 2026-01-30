import os
import sys
import getpass
import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def derive_key_from_passphrase(passphrase, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # ChaCha20 requer uma chave de 32 bytes
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(passphrase.encode())

def encrypt_file(fich):
    passphrase = getpass.getpass("Introduza a passphrase: ")  # Lê a passphrase sem exibi-la
    salt = os.urandom(16)  # Salt de 16 bytes para KDF
    key = derive_key_from_passphrase(passphrase, salt)

    nonce = os.urandom(8)  # Nonce de 8 bytes (alterado)
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    encryptor = cipher.encryptor()

    with open(fich, "rb") as fin:
        plaintext = fin.read()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(fich + ".enc", "wb") as fout:
        fout.write(salt + nonce + ciphertext)

    print(f"Ficheiro cifrado guardado como {fich}.enc")

def decrypt_file(fich):
    passphrase = getpass.getpass("Introduza a passphrase: ")  # Lê a passphrase sem exibi-la

    with open(fich, "rb") as fin:
        salt = fin.read(16)
        nonce = fin.read(8)
        ciphertext = fin.read()

    key = derive_key_from_passphrase(passphrase, salt)
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(fich + ".dec", "wb") as fout:
        fout.write(plaintext)

    print(f"Ficheiro decifrado guardado como {fich}.dec")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: pbenc_chacha20.py <enc|dec> <fich>")
        sys.exit(1)

    operation = sys.argv[1]

    if operation == "enc":
        encrypt_file(sys.argv[2])

    elif operation == "dec":
        decrypt_file(sys.argv[2])

    else:
        print("Operação inválida! Use enc ou dec.")
