import os
import sys
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box

from src import converter
from src import quack
from src import splitter
from src import utils
from src import relatorio

console = Console()

def main_menu():
    while True:
        utils.clear()

        largura = 65 
        gambiarra = 82

        console.print(Panel(
            "📋 [bold green]MENU PRINCIPAL[/bold green] 📋".center(gambiarra),
            width=largura,
            style="cyan",
            title="📂 AjeitaFiles",
            title_align="center",
            padding=(1, 2)
        ))

        # Cria tabela de opções com largura fixa
        table = Table(show_header=False, expand=False, pad_edge=False, box=None)
        table.add_column("Opção", justify="right", style="bold yellow", width=3)
        table.add_column("Descrição", style="bold white", width=largura - 5, no_wrap=True)

        # Adiciona as linhas do menu
        table.add_row("0", "🔌 Finalizar o Programa")
        table.add_row("1", "🔄 Converter Arquivo")
        table.add_row("2", "📊 Relatório de Arquivo")
        table.add_row("3", "🦆 Rodar Query SQL (DuckDB)")
        table.add_row("4", "🔪 Splitter de Arquivos")

        # Imprime tabela dentro de um painel arredondado
        console.print(Panel(table, width=largura, box=box.ROUNDED))

        # Input com cor
        opcao = console.input("\n👉 [bold cyan]Escolha uma opção:[/bold cyan] ")

        if opcao == "0":
            console.print("\n[bold red]Saindo... 👋[/bold red]")
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
