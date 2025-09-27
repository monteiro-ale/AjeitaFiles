import time

def clear():
    import os
    return os.system("cls" if os.name == "nt" else "clear")

def warn(message: str, delay: int = 5):
    print(f"⚠️ {message}")
    time.sleep(delay)

def print_menu(title: str, options: list[str]):
    largura = 65
    print("=" * largura)
    print(title.center(largura))
    print("=" * largura)
    for i, opt in enumerate(options, start=1):
        print(f"{i} - {opt}".ljust(largura))
    print("=" * largura)

def error(message: str, delay: int = 5):
    print(f"❌ {message}")
    if delay:
        time.sleep(delay)

def info(message: str):
    print(f"ℹ️ {message}")
