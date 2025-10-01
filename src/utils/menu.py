import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from src.config.config import *

console = Console()

#Limpa a tela.
def clear():
    import os
    return os.system("cls" if os.name == "nt" else "clear")

#Mensagem de warning.
def warn(message: str, delay: int=5):
    console.print(
        Panel(
            Text(f"{message}", style="yellow"),
            border_style="yellow",
            title="AVISO :warning:",
            expand=False,
            box=box.ROUNDED
        )
    )
    time.sleep(delay)

#Vai cair em breve.. nem deve ta sendo usado
def print_menu_original(title: str, options: list[str]):
    largura = 65
    print("=" * largura)
    print(title.center(largura))
    print("=" * largura)
    for i, opt in enumerate(options, start=1):
        print(f"{i} - {opt}".ljust(largura))
    print("=" * largura)

#Mensagem de erro.
def error(message: str, delay: int = 5):
    console.print(
        Panel(
            Text(f"{message}", style="red"),
            border_style="red",
            title="ERRO :cross_mark:",
            expand=False,
            box=box.ROUNDED
        )
    )
    time.sleep(delay)

#Mensagem de info.
def info(message: str):
    console.print(
        Panel(
            Text(f"{message}", style="blue"),
            border_style="blue",
            title="INFO :information:",
            expand=False,
            box=box.ROUNDED
        )
    )

#Print dos menus.
def print_menu(title: str, options: list[str], style: str = "bold cyan"):
    
    menu_items = []
    for i, opt in enumerate(options, start=0):
        item = f"[{style}]{i}[/{style}] - {opt}"
        menu_items.append(item)

    content = "\n".join(menu_items)

    menu_panel = Panel(
        content,
        title=f" {title} ",
        border_style=style,
        box=box.ROUNDED,
        padding=(1, 2),
        expand=False
    )   
    console.print(menu_panel)

#Print do header de menu.
def print_header(title: str, options: list[str], style: str = "bold", fontstyle: str = "bold"):
    menu_items = []
    for opt in (options):
        item = f"[{fontstyle}]- {opt}"
        menu_items.append(item)

    content = "\n".join(menu_items)

    menu_panel = Panel(
        content,
        title=f" {title} ",
        border_style=style,
        box=box.ROUNDED,
        padding=(1, 2),
        expand=False
    )   
    console.print(menu_panel)

def commands(title: str, options: list[str], style: str = "bold cyan"):
    menu_items = []
    for opt in (options):
        item = f"[{style}]- {opt}"
        menu_items.append(item)

    content = "\n".join(menu_items)

    menu_panel = Panel(
        content,
        title=f" {title} ",
        border_style=style,
        box=box.ROUNDED,
        padding=(1, 2),
        expand=False
    )   
    console.print(menu_panel)