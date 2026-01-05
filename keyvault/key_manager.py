import os
import string
import base64

KEY_FILE = "vault.key"

def load_key_from_path(path: str):
    with open(path, "rb") as f:
        return f.read()

def find_key_locally() -> str | None:
    return KEY_FILE if os.path.exists(KEY_FILE) else None

def find_key_on_removable_drives() -> str | None:
    for letter in string.ascii_uppercase[3:]:  # D:, E:, ...
        drive = f"{letter}:\\"
        key_path = os.path.join(drive, KEY_FILE)
        try:
            if os.path.exists(key_path):
                return key_path
        except OSError:
            continue
    return None

def find_key() -> str | None:
    """Возвращает путь к ключу или None."""
    key_path = find_key_locally()
    if key_path:
        return key_path
    return find_key_on_removable_drives()

def get_raw_key_for_aes(key_b64: bytes) -> bytes:
    """Преобразует base64-ключ Fernet в 32-байтный сырой ключ для AESGCM."""
    return base64.urlsafe_b64decode(key_b64)