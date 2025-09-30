import os
import sys
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box

from .config.config import *
from .conversion import converter
from .duck import quack
from .splitter import splitter
from .utils import menu
from .reports import relatorio

console = Console()

def main_menu():
    while True:
        menu.clear()

        largura = 65 
        #gambiarra = 85 --talvez eu precise de novo

        console.print(Panel(
            "[bold]/📂 AjeitaFiles/[/bold]".center(largura),
            width=largura,
            style=M_HEADER,
            title_align="center",
            padding=(1, 2)
        ))

        # Cria tabela de opções com largura fixa
        table = Table(show_header=False, expand=False, pad_edge=False, box=None, padding=(1,1))
        table.add_column("Opção", justify="right", style=M_MAIN, width=3)
        table.add_column("Descrição", style=M_MAIN, width=largura - 5, no_wrap=True)

        # Adiciona as linhas do menu
        table.add_row("0", "⏩ Finalizar o Programa")
        table.add_row("1", "⏩ Converter Arquivo")
        table.add_row("2", "⏩ Relatório de Arquivo")
        table.add_row("3", "⏩ Rodar Query SQL (DuckDB)")
        table.add_row("4", "⏩ Splitter de Arquivos")

        console.print(Panel(table, 
                            width=largura, 
                            box=box.ROUNDED, 
                            style=M_HEADER, 
                            title="[bold #99C8F2]MENU[/bold #99C8F2]", padding= (1,2)))
                            #padding=(1,2))

        opcao = console.input("\n📌 [bold white]Escolha uma opção:[/bold white] ")

        if opcao == "0":
            console.print("\n[bold yellow]Encerrando... 💤[/bold yellow]")
            time.sleep(1)
            os.system("cls" if os.name == "nt" else "clear")
            break
        elif opcao == "1":
            converter.convert_menu()
        elif opcao == "2":
            relatorio.relatorio_menu()
            time.sleep(1)
        elif opcao == "3":
            quack.pato_menu()
            time.sleep(1)
        elif opcao == "4":
            splitter.split_menu()
            time.sleep(1)
        else:
            console.print("\n⚠️ [bold red]Opção inválida, tente novamente![/bold red]")
            time.sleep(1)
            os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    main_menu()

