import duckdb
from src.config import *
from src.utils import *
import time
from rich.console import Console
from rich.table import Table
console = Console()


def relatorio_menu():
    clear()
    largura = 65
    title = "📊 MODULO RELATÓRIO 📊"

    print("=" * largura)
    print(title.center(largura))
    print("=" * largura)
    files = list_files()
    if files:
        selected = select_file(files)
    else: return
    if selected is None:
        return
    else: exec_relatorio(selected)

def list_files():
    files = list_csv_files()
    if files:
      print("=" * 65)
      print("\n Arquivos disponíveis para análise: (📂 Folder csv):\n")
      for idx, f in enumerate(files, start=1): 
        print(f"{idx} - {f}\n")
      return files
    else:
        return

def select_file(files):
    while True:
        print("=" * 65)
        print("📁 Selecione o arquivos .CSV para gerar relatório")
        print("🔢 Digite o número dos arquivos separados por vírgula")
        print("↩️ Digite \\exit para voltar ao menu anterior")
        print("🗃️ Digite ENTER para selecionar todos os arquivos")
        escolha = input("\n>").strip()

        if escolha == "\\exit":
            return
        if not escolha:
            return files  

        try:
            indices = [int(x.strip()) - 1 for x in escolha.split(",")]
            if any(i < 0 or i >= len(files) for i in indices):
                print("⚠️ Um ou mais números estão fora do intervalo válido.")
                continue

            arquivos_selecionados = [files[i] for i in indices]
            return arquivos_selecionados

        except ValueError:
            print("⚠️ Entrada inválida. Digite apenas números separados por vírgula.")

def exec_relatorio(selected):
    for file in selected:
        filepath = CSV_DIR / file
        table_name = os.path.splitext(file)[0]  # tira o .csv
        diagnostico_duckdb(filepath, table_name)

def diagnostico_duckdb(filepath, table_name="tabela"):
    con = duckdb.connect()

    # Carrega o CSV como uma tabela
    con.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{str(filepath)}', header=True, SAMPLE_SIZE=-1)
    """)
    console.print(f"📂 Arquivo [bold]{filepath}[/bold] carregado com sucesso!\n", style="green")
    printa_diagnostico(con, table_name)

def printa_diagnostico(con, table_name):
    cols = count_lines_and_columns(con, table_name)
    constant_columns(con,cols, table_name)
    column_cardinality(con, cols, table_name)
    column_null(con, cols, table_name)


def count_lines_and_columns(con, table_name):
    # Número de linhas e colunas
    shape = con.execute(f"SELECT COUNT(*) AS linhas FROM {table_name}").fetchone()[0]
    cols = con.execute(f"PRAGMA table_info({table_name})").fetchall()
    console.print(f"Linhas: [bold]{shape:,}[/bold]")
    console.print(f"Colunas: [bold]{len(cols)}[/bold]\n")
    return cols

def constant_columns(con, cols, table_name):  
    constantes = []
    for c in cols:
        col = c[1]
        distincts = con.execute(f'SELECT COUNT(DISTINCT "{col}") FROM "{table_name}"').fetchone()[0]
        if distincts == 1:
            constantes.append(col)

    table_const = Table(title="🔹 Colunas constantes", show_lines=True)
    table_const.add_column("Coluna", style="cyan")
    if constantes:
        for col in constantes:
            table_const.add_row(col)
    else:
        table_const.add_row("Nenhuma coluna constante encontrada")
    console.print(table_const)
    console.print()
    console.print("📌 Pressione [bold green]ENTER[/bold green] para continuar para a próxima seção...", style="yellow")
    input()

def column_cardinality(con, cols, table_name):
    table_card = Table(title="🔹 Cardinalidade (nº de valores únicos por coluna)", show_lines=True)
    table_card.add_column("Coluna", style="magenta")
    table_card.add_column("Valores únicos", justify="right", style="yellow")
    for c in cols:
        col = c[1]
        nuniq = con.execute(f'SELECT COUNT(DISTINCT "{col}") FROM "{table_name}"').fetchone()[0]
        table_card.add_row(col, f"{nuniq:,}")
    console.print(table_card)
    console.print()
    console.print("📌 Pressione [bold green]ENTER[/bold green] para continuar para a próxima seção...", style="yellow")
    input()

def column_null(con, cols, table_name):    # Valores nulos por coluna
    table_null = Table(title="🔹 Valores nulos por coluna", show_lines=True)
    table_null.add_column("Coluna", style="red")
    table_null.add_column("Nulos", justify="right", style="bright_red")
    for c in cols:
        col = c[1]
        nnulos = con.execute(f'SELECT COUNT(*) FROM "{table_name}" WHERE "{col}" IS NULL').fetchone()[0]
        table_null.add_row(col, f"{nnulos:,}")
    console.print(table_null)
    console.print()
    console.print("📌 Pressione [bold green]ENTER[/bold green] para continuar para a próxima seção...", style="yellow")
    input()

    time.sleep(10)
    con.close()




#Se quiser que zero e vazio sejam considerados diferentes (colunas constantes).
#SELECT COUNT(DISTINCT COALESCE(CAST(COL1 AS VARCHAR), 'NULL_REPLACEMENT')) 
#FROM tabela;
