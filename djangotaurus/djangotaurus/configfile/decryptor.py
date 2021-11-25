import hashlib
import os
import pyaes


class Decryptor():

    @staticmethod
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

    @staticmethod
    def aes_decrypt(line, pwd):
        key = bytes(bytearray.fromhex(os.environ.get('key')))
        iv = bytes(bytearray.fromhex(os.environ.get('iv')))

        # Decryption with AES-256-CBC
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
        decrypted_data = decrypter.feed(bytes(bytearray.fromhex(line)))
        decrypted_data += decrypter.feed()

        return decrypted_data.decode('utf-8')

    @staticmethod
    def decrypt_file(file):
        key = os.environ.get('key')
        plaintext_values = {}
        secret_values = Decryptor.file_read(file)
        for k, v in secret_values.items():
            plaintext_values[k] = Decryptor.aes_decrypt(v, key)

        return plaintext_values


