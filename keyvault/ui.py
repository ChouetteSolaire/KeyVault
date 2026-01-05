import inquirer

import inquirer

def show_menu() -> str | None:
    questions = [
        inquirer.List(
            'action',
            message="Выберите действие",
            choices=[
                "Создать новый сейф и ключ",
                "Добавить файл в сейф",
                "Извлечь файл из сейфа",
                "Показать список файлов",
                "Выход"
            ]
        )
    ]
    ans = inquirer.prompt(questions)
    return ans['action'] if ans else None

def ask_file_path() -> str | None:
    q = [inquirer.Text('path', message="Путь к файлу")]
    ans = inquirer.prompt(q)
    return ans['path'].strip() if ans else None

def ask_file_selection(choices: list[str]) -> str | None:
    if not choices:
        return None
    q = [inquirer.List('file', message="Выберите файл", choices=choices)]
    ans = inquirer.prompt(q)
    return ans['file'] if ans else None

def pause():
    input("\nНажмите Enter, чтобы продолжить...")

def print_error(msg: str):
    print(f"❌ {msg}")
    pause()

def print_success(msg: str):
    print(f"✅ {msg}")
    pause()

def print_info(msg: str):
    print(f"🔍 {msg}")