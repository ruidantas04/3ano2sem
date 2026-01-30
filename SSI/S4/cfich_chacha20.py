import struct
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_key(fkey):
    key = os.urandom(32)
    with open(fkey, "wb") as f:
        f.write(key)
    print(f"Chave gerada e guardada em {fkey}")

def encrypt_file(fich, fkey):
    with open(fkey, "rb") as f:
        key= f.read(32)

    nonce = os.urandom(8)
    counter = 0
    full_nonce = struct.pack("<Q", counter) + nonce
    algorithm = algorithms.ChaCha20(key, full_nonce)
    cipher = Cipher(algorithm, mode=None)
    encryptor = cipher.encryptor()

    with open(fich, "rb") as fin, open(fich + ".enc", "wb") as fout:
        fout.write(nonce)
        fout.write(encryptor.update(fin.read()) + encryptor.finalize())

    print(f"Ficheiro cifrado guardado como {fich}.enc")

def decrypt_file(fich, fkey):
    with open(fkey, "rb") as f:
        key= f.read(32)
    with open(fich, "rb") as fin:
        nonce = fin.read(8)
        counter = 0
        full_nonce = struct.pack("<Q", counter) + nonce
        algorithm = algorithms.ChaCha20(key, full_nonce)
        cipher = Cipher(algorithm, mode=None)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(fin.read()) + decryptor.finalize()

    with open(fich + ".dec", "wb") as fout:
        fout.write(decrypted_data)

    print(f"Ficheiro decifrado guardado como {fich}.dec")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Uso: cfich_chacha20.py <setup|enc|dec> <fich> [<fkey>]")
        sys.exit(1)

    operation = sys.argv[1]

    if operation == "setup":
        fkey = sys.argv[2]
        generate_key(fkey)

    elif operation == "enc":
        if len(sys.argv) < 4:
            print("Uso: cfich_chacha20.py enc <fich> <fkey>")
            sys.exit(1)
        encrypt_file(sys.argv[2], sys.argv[3])

    elif operation == "dec":
        if len(sys.argv) < 4:
            print("Uso: cfich_chacha20.py dec <fich> <fkey>")
            sys.exit(1)
        decrypt_file(sys.argv[2], sys.argv[3])

    else:
        print("Operação inválida! Use setup, enc ou dec.")
