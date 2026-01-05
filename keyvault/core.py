from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Метки методов
METHOD_FERNET = b'\x01'
METHOD_AESGCM = b'\x02'

def encrypt_file_fernet(key: bytes, data: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_file_fernet(key: bytes, data: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(data)

def encrypt_file_aesgcm(key: bytes, data: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return nonce + ciphertext  # сохраняем nonce вместе с данными

def decrypt_file_aesgcm(key: bytes, data: bytes) -> bytes:
    nonce = data[:12]
    ciphertext = data[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)

def encrypt_file(method: str, key: bytes, input_path: str, output_path: str):
    with open(input_path, "rb") as f:
        data = f.read()

    if method == "fernet":
        encrypted = encrypt_file_fernet(key, data)
        full_data = METHOD_FERNET + encrypted
    elif method == "aes256gcm":
        encrypted = encrypt_file_aesgcm(key, data)
        full_data = METHOD_AESGCM + encrypted
    else:
        raise ValueError("Неизвестный метод шифрования")

    with open(output_path, "wb") as f:
        f.write(full_data)

def decrypt_file(key: bytes, input_path: str, output_path: str):
    with open(input_path, "rb") as f:
        full_data = f.read()

    method_byte = full_data[0:1]
    encrypted = full_data[1:]

    if method_byte == METHOD_FERNET:
        decrypted = decrypt_file_fernet(key, encrypted)
    elif method_byte == METHOD_AESGCM:
        decrypted = decrypt_file_aesgcm(key, encrypted)
    else:
        raise ValueError("Неизвестный метод шифрования")

    with open(output_path, "wb") as f:
        f.write(decrypted)