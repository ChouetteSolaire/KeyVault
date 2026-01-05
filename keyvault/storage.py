import os

VAULT_DIR = "vault"

def ensure_vault_exists():
    os.makedirs(VAULT_DIR, exist_ok=True)

def get_encrypted_files():
    """Возвращает список имён зашифрованных файлов без .enc"""
    ensure_vault_exists()
    files = os.listdir(VAULT_DIR)
    return [f[:-4] for f in files if f.endswith(".enc")]

def get_encrypted_path(filename: str) -> str:
    return os.path.join(VAULT_DIR, filename + ".enc")

