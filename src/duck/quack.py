import duckdb
import os
from src.config.config import CSV_DIR, BASE_DIR
from src.utils.utils import *
from src.utils.menu import *
from rich.console import Console
from rich.table import Table
from rich import box
import math

console = Console()


def pato_menu():
    clear()
    title = ":duck: MODULO DUCKDB :duck:"
    opt = [
       "Voltar ao menu anterior",
       "Importar CSV para o banco persistente (:optical_disk: disco)",
       "Carregar CSV temporariamente na RAM (:floppy_disk: in-memory)",
       "Usar tabelas já existentes no banco persistente :file_cabinet:"      
    ]

    print_menu(title, opt, "bold yellow")
    print("Escolha uma das opções acima:\n")
    e = input(">").strip()
    if e in ("4", "\\exit", "exit", "0"):
        return
    elif e == "1":
        clear()
        persistence = True
        importa_csv_banco(persistence)
    elif e == "2":
        clear()
        persistence = False
        importa_csv_banco(persistence)
        return
    elif e == "3":
      path = f"{BASE_DIR}"+"\\ajeitafiles.duckdb"
      con = conectar_duckdb(path)
      loop_interativo(con)
      return
    else:
        warn("Opção inválida, digite apenas números",1)
        return

def importa_csv_banco(persistence):

    con = conectar_duckdb(f"{BASE_DIR}\\ajeitafiles.duckdb")
    if not con:
        return

    tables = get_db_tables(con)
    if not tables:
        warn("Nenhuma tabela salva no banco persistente.", 0)

    files = get_csv_files()
    if not files:
        warn("Nenhum arquivo encontrado na folder CSV.")

    list_all(tables, files)
    arquivos = handle_user_choice(files)
    if not arquivos:
        return
    processed = process_files(con, arquivos, persistence)
    if not processed:
        return
    mostrar_arquivos_carregados(arquivos)
    loop_interativo(processed)


#function inutil, tirar depois
def mostrar_arquivos_carregados(arquivos):
    print("=" * 60)
    print("⚡ Arquivos carregados em memória:")
    for arq in arquivos:
        print(f"- {arq}")
    print("=" * 60)

def list_all(tables, files):
    if tables:
      try:
        for t in (tables): print(f"- {t}\n")
      except: print("Erro ao listar tabelas do banco")
    if files:
        print("=" * 65)
        print("\n📂 Arquivos disponíveis para carregar em memória (📂 Folder csv):\n")
        for idx, f in enumerate(files, start=1): 
          print(f"{idx} - {f}\n")
    else:
        return

#Lista as tabelas do database.
def list_db_tables(con):
    try:
        tables = con.execute("SHOW TABLES").fetchall()
        if not [t[0] for t in tables]:
            print("Sem tabelas salvas no banco persistente")
            return
        else:
          print("="*65)
          print("💾 Tabelas já existentes no banco:".center(65))
          print("="*65)
          print("\n")
        return [t[0] for t in tables]
    except Exception as e:
        print(f"Erro ao listar tabelas no banco.{e}")
        return None

def conectar_duckdb(db_path):
        try:
            return duckdb.connect(database=db_path)
        except Exception as e:
            print(f"Erro ao conectar ao DuckDB: {e}")
            #print("Diretório atual:", os.getcwd()) # Caso o db de o perdido
            time.sleep(10)
            return None

def handle_user_choice(files):
    while True:
        print("=" * 65)
        print("📁 Selecione os arquivos CSV para carregar")
        print("🔢 Digite os números dos arquivos separados por vírgula")
        print("↩️ Digite \\exit para voltar ao menu anterior")
        print("*️⃣ Digite ENTER para selecionar todos os arquivos")
        escolha = input("\n>").strip()

        if escolha == "\\exit":
            return None
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

def process_files(con, arquivos, persistence):
      if persistence:
        query = "CREATE OR REPLACE TABLE"
      else:
        query = "CREATE OR REPLACE TEMP TABLE"
      try:
          for arq in arquivos:
            caminho = os.path.join(CSV_DIR, arq)
            nome_tabela = os.path.splitext(arq)[0]
            con.execute(
            f"""{query} {nome_tabela} AS SELECT * FROM read_csv_auto('{caminho}', sample_size=-1)"""
            )
            print(f"[OK] Tabela carregada: {nome_tabela}")
          return con
      except Exception as e:
          print(f"Erro ao carregar {arq}: {e}")
          time.sleep(5)
          clear()
          return None

def loop_interativo(con):
    clear()
    print("=" * 65)
    print("\nDigite queries SQL (\\exit para sair, \\tables para listar tabelas, \\export para exportar última consulta)\n")
    print("Use \\next e \\prev para navegar em resultados grandes.\n")
    print("=" * 65)
    
    last_df = None
    current_page = 0
    page_size = 20

    while True:
        query = input("SQL> ").strip()
        
        if query.lower() in ["\\exit", "exit", "quit"]:
            print("Saindo do módulo SQL...")
            break

        elif query.lower() in ["\\tables", ".tables"]:
            tabelas = con.execute("SHOW TABLES").fetchall()
            print("Tabelas carregadas:", [t[0] for t in tabelas])

        elif query.lower().startswith("\\export"):
            if last_df is None:
                print("Nenhuma consulta para exportar ainda.")
            else:
                parts = query.split(maxsplit=1)
                filename = f"{parts[1]}.csv" if len(parts) > 1 else "last_query.csv"
                path = f"{CSV_DIR}\\{filename}"
                last_df.to_csv(path, index=False)
                print(f"Última consulta exportada para {path}")

        elif query.lower() == "\\next":
            if last_df is not None:
                total_pages = math.ceil(len(last_df) / page_size)
                if current_page < total_pages - 1:
                    current_page += 1
                    print_page(last_df, current_page, page_size)
                else:
                    print("⚠️ Já está na última página.")
            else:
                print("Nenhum resultado carregado ainda.")

        elif query.lower() == "\\prev":
            if last_df is not None:
                if current_page > 0:
                    current_page -= 1
                    print_page(last_df, current_page, page_size)
                else:
                    print("⚠️ Já está na primeira página.")
            else:
                print("Nenhum resultado carregado ainda.")

        elif query:
            try:
                df = con.execute(query).df()
                last_df = df
                current_page = 0
                print_page(last_df, current_page, page_size)
            except Exception as e:
                print(f"Erro: {e}")

def print_page(df, page, page_size=20):
    start = page * page_size
    end = start + page_size
    subset = df.iloc[start:end]
#table = Table(show_header=True, header_style="bold magenta", show_lines=True, box=box.SIMPLE_HEAVY)
    table = Table(show_header=True, header_style="bold magenta")
    for col in subset.columns:
        table.add_column(str(col), overflow="fold")

    for _, row in subset.iterrows():
        table.add_row(*[str(val) if val is not None else "" for val in row.values])

    console.print(table)
    print(f"\n📊 Mostrando linhas {start+1}–{min(end, len(df))} de {len(df)} (página {page+1}/{math.ceil(len(df)/page_size)})\n")
