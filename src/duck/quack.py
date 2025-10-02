import duckdb
import os
from src.config.config import *
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

    print_menu(title, opt, M_DUCK)
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
      exec_sql_query(con)
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
    exec_sql_query(processed)

#Lista as tabelas do database e os arquivos da folder csv.
def list_all(tables, files):
    opt = [
      "Digite os números dos arquivos separados por vírgula",
      "Digite \\exit para voltar ao menu anterior",
      "Digite ENTER para selecionar todos os arquivos"            
      ]
    if tables:
      try:
        print_header(":duck: MODULO DUCKDB :duck:", opt, M_DUCK, M_CONFIG)
        print_header(":optical_disk: Tabelas já existentes no database:", tables, M_DUCK, M_CONFIG)
      except: error("Erro ao listar tabelas do banco")
    if files:
        print_menu(":file_folder: Arquivos disponíveis(Folder/csv/):", files, M_DUCK)
    else:
        return

def conectar_duckdb(db_path):
        try:
            return duckdb.connect(database=db_path)
        except Exception as e:
            error(f"Erro ao conectar ao DuckDB: {e}", 2)
            time.sleep(10)
            return None

def handle_user_choice(files):
    while True:
        escolha = input("\n>").strip()

        if escolha in ("\\exit", "exit"):
            return None
        if not escolha:
            return files  
        try:
            indices = [int(x.strip()) for x in escolha.split(",")]
            if any(i < 0 or i >= len(files) for i in indices):
                warn("Um ou mais números estão fora do intervalo válido.")
                continue
            arquivos_selecionados = [files[i] for i in indices]
            return arquivos_selecionados
        except ValueError:
            warn("Entrada inválida. Digite apenas números separados por vírgula.")

def exec_sql_query(con):
    last_df = None
    current_page = 0
    page_size = 20
    
    clear()
    print("=" * 65)
    print("\n[  MÓDULO SQL INTERATIVO  ]\n")
    print("Comandos: \\exit, \\tables, \\export, \\next, \\prev\n")
    print("=" * 65)

    while True:
        query = input("SQL> ").strip()
        command = query.lower().split()[0] if query.startswith("\\") else None
        
        #Comandos
        if command == "\\exit":
            print("Saindo do módulo SQL...")
            break
        elif command == "\\tables":
            display_tables(con)
        elif command == "\\export":
            export_last_query(last_df, query)
        elif command == "\\next":
            current_page = handle_navigation(last_df, current_page, page_size, "next")
        elif command == "\\prev":
            current_page = handle_navigation(last_df, current_page, page_size, "prev")
            
        #Queries
        elif query:
            # handle_sql_query retorna uma tupla (df, page_num)
            df_novo, page_nova = handle_sql_query(con, query, page_size)           
            if df_novo is not None:
                last_df = df_novo
                current_page = page_nova

def display_tables(con):
    try:
        tabelas = con.execute("SHOW TABLES").fetchall()
        print("Tabelas carregadas:", [t[0] for t in tabelas])
    except Exception as e:
        error(f"Erro ao listar tabelas: {e}")

def handle_sql_query(con, query, page_size):
    try:
        df = con.execute(query).df()
        current_page = 0
        print_page(df, current_page, page_size)
        return df, current_page
    except Exception as e:
        print(f"Erro na Query: {e}")
        # Retorna None, None para indicar falha e não atualizar o estado
        return None, None

def handle_navigation(last_df, current_page, page_size, direction):
    if last_df is None or last_df.empty:
        print("Nenhum resultado carregado ainda para navegar.")
        return current_page
    
    total_pages = math.ceil(len(last_df) / page_size)
    
    if direction == "next":
        if current_page < total_pages - 1:
            new_page = current_page + 1
        else:
            print("⚠️ Já está na última página.")
            new_page = current_page
            
    elif direction == "prev":
        if current_page > 0:
            new_page = current_page - 1
        else:
            print("⚠️ Já está na primeira página.")
            new_page = current_page
            
    if new_page != current_page:
        print_page(last_df, new_page, page_size)   
    return new_page

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

def print_page(df, page, page_size=20):
    start = page * page_size
    end = start + page_size
    subset = df.iloc[start:end]
    table = Table(show_header=True, header_style="bold magenta")
    for col in subset.columns:
        table.add_column(str(col), overflow="fold")

    for _, row in subset.iterrows():
        table.add_row(*[str(val) if val is not None else "" for val in row.values])

    console.print(table)
    print(f"\n📊 Mostrando linhas {start+1}–{min(end, len(df))} de {len(df)} (página {page+1}/{math.ceil(len(df)/page_size)})\n")
    return

def export_last_query(last_df, query):
    if last_df is None:
      print("Nenhuma consulta para exportar ainda.")
    else:
        parts = query.split(maxsplit=1)
        filename = f"{parts[1]}.csv" if len(parts) > 1 else "last_query.csv"
        path = f"{CSV_DIR}\\{filename}"
        last_df.to_csv(path, index=False)
        print(f"Última consulta exportada para {path}")

