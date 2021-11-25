import hashlib
import os
import pyaes


def file_read(file):
    values = {}
    f = open(file)
    for line in f:
        line = line.rstrip(',\n')
        line = line.replace('"', '')
        key = line.split('=')[0]
        value = line.split('=')[1]
        values[key] = value
    return values


def file_replace(ciphertext):
    file_path = "../../.env"

    f = open(file_path, "w")
    for k, v in ciphertext.items():
        f.write('"'+k+'"'+'="'+v+'"\n')
    f.close()


def aes_encrypt(line, pwd):
    password = str.encode(pwd)
    salt = bytes(bytearray.fromhex(os.environ.get('salt')))
    iterationCount = 10000
    iv = bytes(bytearray.fromhex(os.environ.get('iv')))

    # Create 32 bytes key
    key = hashlib.pbkdf2_hmac('sha256', password, salt, iterationCount)

    # Encryption with AES-256-CBC
    encryptor = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(key, iv))
    ciphertext = encryptor.feed(line.encode('utf8'))
    ciphertext += encryptor.feed()

    return ciphertext.hex()


def encrypt_file(file):
    encrypted_values = {}
    secret_values = file_read(file)
    for k, v in secret_values.items():
        encrypted_values[k] = aes_encrypt(v, os.environ.get('pass'))
    file_replace(encrypted_values)


encrypt_file("creds")