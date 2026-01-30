import os
import sys


def generate_key(size, filename):
    key = os.urandom(size)  # Gera bytes aleatórios
    with open(filename, "wb") as f:
        f.write(key)


def xor_bytes(data, key):
    return bytes(a ^ b for a, b in zip(data, key))


def encrypt(input_file, key_file):
    with open(input_file, "rb") as f:
        plaintext = f.read()
    with open(key_file, "rb") as f:
        key = f.read()
    if len(key) < len(plaintext):
        raise ValueError("A chave deve ser pelo menos do mesmo tamanho que o texto!")
    ciphertext = xor_bytes(plaintext, key)
    output_file = input_file + ".enc"
    with open(output_file, "wb") as f:
        f.write(ciphertext)
    print(f"Mensagem cifrada em {output_file}")


def decrypt(input_file, key_file):
    with open(input_file, "rb") as f:
        ciphertext = f.read()
    with open(key_file, "rb") as f:
        key = f.read()
    if len(key) < len(ciphertext):
        raise ValueError("A chave deve ser pelo menos do mesmo tamanho que a cifra!")
    plaintext = xor_bytes(ciphertext, key)
    output_file = input_file + ".dec"
    with open(output_file, "wb") as f:
        f.write(plaintext)
    print(f"Mensagem decifrada em {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python otp.py [setup|enc|dec] args...")
        sys.exit(1)

    command = sys.argv[1]

    if command == "setup" and len(sys.argv) == 4:
        generate_key(int(sys.argv[2]), sys.argv[3])
    elif command == "enc" and len(sys.argv) == 4:
        encrypt(sys.argv[2], sys.argv[3])
    elif command == "dec" and len(sys.argv) == 4:
        decrypt(sys.argv[2], sys.argv[3])
    else:
        print("Comando inválido!")
        sys.exit(1)
