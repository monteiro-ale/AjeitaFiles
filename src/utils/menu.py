import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

def clear():
    import os
    return os.system("cls" if os.name == "nt" else "clear")

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

def print_menu_original(title: str, options: list[str]):
    largura = 65
    print("=" * largura)
    print(title.center(largura))
    print("=" * largura)
    for i, opt in enumerate(options, start=1):
        print(f"{i} - {opt}".ljust(largura))
    print("=" * largura)

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

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

def print_menu(title: str, options: list[str], style: str = "bold cyan"):
    
    # 1. Constrói o conteúdo do menu (as opções)
    menu_items = []
    for i, opt in enumerate(options, start=0):
        # Usa Markup do Rich para colorir o número
        item = f"[bold green]{i}[/bold green] - {opt}"
        menu_items.append(item)

    # 2. Junta tudo com quebras de linha
    content = "\n".join(menu_items)

    # 3. Cria o Panel
    menu_panel = Panel(
        content,
        title=f" {title} ",  # Título no topo
        border_style=style,
        box=box.ROUNDED,          # Bordas mais robustas
        padding=(1, 2),         # Adiciona um pouco de espaço interno
        expand=False            # O Panel só terá a largura necessária
    )
    
    console.print(menu_panel)

# # --- Exemplo de Uso ---
# print_menu_panel(
#     "MENU PRINCIPAL",
#     ["Carregar e Validar CRM", "Gerar Relatório de Qualidade", "Configurações", "Sair (0)"]
# )