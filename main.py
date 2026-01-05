import os
import inquirer
from keyvault import core, storage, key_manager, ui
from cryptography.fernet import Fernet

KEY_FILE = "vault.key"
VAULT_DIR = "vault"

def init_vault():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    ui.print_success("Сейф и ключ созданы!\n"
                     f"📁 Папка: {VAULT_DIR}\n"
                     f"🔑 Ключ: {KEY_FILE}\n"
                     "👉 Перенесите этот файл на флешку и удалите с компьютера!")

def add_file():
    filepath = ui.ask_file_path()
    if not filepath or not os.path.exists(filepath):
        ui.print_error("Файл не найден!")
        return

    method_q = [
        inquirer.List(
            'method',
            message="Выберите метод шифрования",
            choices=[
                ("Fernet (AES-128 + HMAC, простой)", "fernet"),
                ("AES-256-GCM (современный, с аутентификацией)", "aes256gcm")
            ]
        )
    ]
    method_ans = inquirer.prompt(method_q)
    if not method_ans:
        return
    method = method_ans['method']

    key_path = key_manager.find_key()
    if not key_path:
        ui.print_error("Ключ не найден ни в папке, ни на флешках!")
        return

    try:
        key = key_manager.load_key_from_path(key_path)

        # Подготовка ключа в зависимости от метода
        if method == "aes256gcm":
            try:
                raw_key = key_manager.get_raw_key_for_aes(key)
            except Exception:
                ui.print_error("Неверный формат ключа. Создайте новый сейф.")
                return
        else:
            raw_key = key

        filename = os.path.basename(filepath)
        output_path = os.path.join(VAULT_DIR, filename + ".enc")
        core.encrypt_file(method, raw_key, filepath, output_path)
        ui.print_success(f"Файл зашифрован ({method}) и сохранён: {output_path}")
    except Exception as e:
        ui.print_error(f"Ошибка шифрования: {e}")


def get_file():
    storage.ensure_vault_exists()
    choices = storage.get_encrypted_files()
    if not choices:
        ui.print_info("📭 Сейф пуст.")
        return

    chosen = ui.ask_file_selection(choices)
    if not chosen:
        return

    encrypted_path = storage.get_encrypted_path(chosen)

    key_path = key_manager.find_key()
    if not key_path:
        ui.print_error("Ключ не найден!")
        return

    try:
        # Читаем метод шифрования
        with open(encrypted_path, "rb") as f:
            method_byte = f.read(1)

        key_b64 = key_manager.load_key_from_path(key_path)

        if method_byte == core.METHOD_AESGCM:
            try:
                key = key_manager.get_raw_key_for_aes(key_b64)
            except Exception:
                ui.print_error("Неверный формат ключа для AES-GCM.")
                return
        else:
            key = key_b64

        output_path = chosen + ".restored"
        core.decrypt_file(key, encrypted_path, output_path)

        # ✅ УДАЛЯЕМ зашифрованный файл после успешной расшифровки
        os.remove(encrypted_path)

        ui.print_success(f"Файл расшифрован и удалён из сейфа: {output_path}")
    except Exception as e:
        ui.print_error(f"Ошибка расшифровки: {e}")

def list_files():
    storage.ensure_vault_exists()
    files = storage.get_encrypted_files()
    if files:
        print("\n📁 Файлы в сейфе:")
        for f in files:
            print(f"  • {f}")
    else:
        print("\n📭 Сейф пуст.")
    ui.pause()

def main():
    storage.ensure_vault_exists()
    while True:
        action = ui.show_menu()
        if not action:
            break
        if action == "Создать новый сейф и ключ":
            init_vault()
        elif action == "Добавить файл в сейф":
            add_file()
        elif action == "Извлечь файл из сейфа":
            get_file()
        elif action == "Показать список файлов":
            list_files()
        elif action == "Выход":
            print("\n👋 До новых встреч!")
            break

if __name__ == "__main__":
    main()