import duckdb
from src.config.config import *
from src.utils.utils import *
from src.utils.menu import *
import time
from rich.console import Console
from rich.table import Table
import sys
console = Console()


def relatorio_menu():
    clear()
    files = list_files()
    if files:
        selected = select_file(files)
    else:
        warn("Não encontrei arquivos no diretório: 📂 AjeitaFiles/data/csv/:") 
        return
    if selected is None:
        return
    else: exec_relatorio(selected)

def list_files():
    files = get_csv_files()
    if files:
      title = "📊 MODULO RELATÓRIO 📊"
      com = [
        "Digite o número dos arquivos separados por vírgula",
        "Digite \\exit para voltar ao menu anterior",
        "Digite ENTER para selecionar todos os arquivos"
      ]
      print_header(title, com, M_REPORT, M_CONFIG)
      return files
    else:
        return

def select_file(files):
    while True:
        print_menu("📁 Selecione o(s) arquivo(s) para gerar relatório", files, M_REPORT)
        info("Arquivos listados no path: 📂 AjeitaFiles/data/csv/:")
        escolha = input("\n>").strip()

        if escolha == "\\exit":
            return
        if not escolha:
            return files  

        try:
            indices = [int(x.strip()) for x in escolha.split(",")]
            if any(i < 0 or i >= len(files) for i in indices):
                print("⚠️ Um ou mais números estão fora do intervalo válido.")
                #clear()
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

    con.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{str(filepath)}', header=True, SAMPLE_SIZE=-1)
    """)
    console.print(f"📂 Arquivo [bold]{filepath}[/bold] carregado com sucesso!\n", style="green")
    printa_diagnostico(con, table_name)

def printa_diagnostico(con, table_name):
    clear()
    cols = preview_table(con, table_name)
    count_lines_and_columns(con, table_name, cols)
    input_keys(con, cols, table_name)
    constant_columns(con,cols, table_name)
    column_cardinality(con, cols, table_name)
    column_null(con, cols, table_name)

def input_keys(con, cols, table_name):
    lower_colnames = [c.strip().lower() for c in cols]

    console.print("🔑 Informe as colunas-chave para verificar duplicidade")
    console.print("   - Digite os nomes separados por vírgula (ex: ID,EMAIL)")
    console.print("   - Pressione ENTER para pular\n", style="yellow")
    key_input = input("> ").strip().lower()
    print("\n")
    table_dupes = Table(title="🔹 Duplicidades", show_lines=True)
    table_dupes.add_column("Resultado", style="bold cyan")

    if key_input:
        keys = [k.strip() for k in key_input.split(",") if k.strip() in lower_colnames]

        if not keys:
            table_dupes.add_row("⚠️ Nenhuma chave válida informada")
        else:
            keys_str = ", ".join([
                f"COALESCE(NULLIF(TRIM(LOWER(CAST(\"{k}\" AS VARCHAR))), ''), '∅')" 
                for k in keys
            ])

            # Filtrar inválidas: todas as chaves obrigatórias não podem ser vazias ou nulas
            where_clause = " AND ".join([
                f"TRIM(CAST(\"{k}\" AS VARCHAR)) <> '' AND \"{k}\" IS NOT NULL"
                for k in keys
            ])
            row = exec_sql_duplicty(con, table_name, where_clause, keys_str)

            total_duplicadas, excedentes = row if row else (0, 0)
            total_duplicadas = total_duplicadas or 0
            excedentes = excedentes or 0

            table_dupes.add_row(
                f"Linhas duplicadas (total): {total_duplicadas:,} "
                f"(Chaves: {', '.join(keys)})"
            )
            table_dupes.add_row(
                f"Linhas excedentes (rejeitadas): {excedentes:,} "
                f"(Chaves: {', '.join(keys)})"
            )
    else:
        #Alea iacta est...
        table_dupes.add_row("Linhas duplicadas: 0 (Colunas-chave não informadas)")

    console.print(table_dupes)
    console.print()
    console.print(
        "📌 Pressione [bold green]ENTER[/bold green] para continuar...", style="yellow"
    )

def exec_sql_duplicty(con, table_name, where_clause, keys_str):
    row = con.execute(f"""
    WITH valid AS (
        SELECT *
        FROM {table_name}
        WHERE {where_clause}
    )
    SELECT
        SUM(cnt) AS total_duplicadas,
        SUM(cnt - 1) AS excedentes
    FROM (
        SELECT COUNT(*) AS cnt
        FROM valid
        GROUP BY {keys_str}
        HAVING COUNT(*) > 1
    )
    """).fetchone()
    return row

def preview_table(con, table_name, max_rows=4, max_cols=10):
    cols = [c[1] for c in con.execute(f"PRAGMA table_info({table_name})").fetchall()]

    if len(cols) <= max_cols:
        rows = con.execute(f"SELECT * FROM {table_name} LIMIT {max_rows}").fetchall()

        table = Table(show_header=True, title="Preview de Colunas", header_style="bold magenta")
        for col in cols:
            table.add_column(col, overflow="fold")

        for row in rows:
            table.add_row(*[str(r) for r in row])

        console.print(table)
    else:
        # Se for muita coluna, mostra só a lista organizada.
        col_text = ", ".join(cols)
        console.print(
            Panel(col_text, title="Preview de Colunas", border_style="cyan", expand=False)
        )
    return cols

def count_lines_and_columns(con, table_name, cols):
    n_rows = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    info = Table(title="Informações da Tabela", show_header=False, box=None)
    info.add_row("Linhas", f"[bold]{n_rows:,}[/bold]")
    info.add_row("Colunas", f"[bold]{len(cols)}[/bold]")

def constant_columns(con, cols, table_name):  
    constantes = []
    for c in cols:
        distincts = con.execute(f'SELECT COUNT(DISTINCT "{c}") FROM "{table_name}"').fetchone()[0]
        if distincts == 1:
            constantes.append(c)

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
        nuniq = con.execute(f'SELECT COUNT(DISTINCT "{c}") FROM "{table_name}"').fetchone()[0]
        table_card.add_row(c, f"{nuniq:,}")
    console.print(table_card)
    console.print()
    console.print("📌 Pressione [bold green]ENTER[/bold green] para continuar para a próxima seção...", style="yellow")
    input()

def column_null(con, cols, table_name):    # Valores nulos por coluna
    table_null = Table(title="🔹 Valores nulos por coluna", show_lines=True)
    table_null.add_column("Coluna", style="red")
    table_null.add_column("Nulos", justify="right", style="bright_red")
    for c in cols:
        nnulos = con.execute(f'SELECT COUNT(*) FROM "{table_name}" WHERE "{c}" IS NULL').fetchone()[0]
        table_null.add_row(c, f"{nnulos:,}")
    console.print(table_null)
    console.print()
    console.print("📌 Pressione [bold green]ENTER[/bold green] para continuar para a próxima seção...", style="yellow")
    input()

    time.sleep(1)
    con.close()



