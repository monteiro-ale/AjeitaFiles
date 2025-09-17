import duckdb
import os
from src.config import CSV_DIR, BASE_DIR
from src.utils import *

def pato_menu():
    clear()
    largura = 65
    title = "MODULO DUCKDB"

    print("=" * largura)
    print(title.center(largura))
    print("=" * largura)
    print("\n📂 MENU INICIAL")
    print("Escolha uma das opções abaixo:\n")
    print("1 - Importar CSV para o banco persistente (💾 disco)")
    print("2 - Carregar CSV temporariamente na RAM (⚡ in-memory)")
    print("3 - Usar tabelas já existentes no banco persistente")
    print("4 - Voltar ao menu anterior\n")
    print("=" * 65)
    e = input(">").strip()
    if e == "4":
        return
    elif e == "1":
        clear()
        importa_csv_banco()
    elif e == "2":
        print(">>Ainda não implementado")
        time.sleep(3)
        return
    elif e == "3":
      print(">>Ainda não implementado")
      time.sleep(3)
      return
    else:
        print("Opção inválida, digite apenas números")
        return

def importa_csv_banco():
    path = f"{BASE_DIR}"+"\\ajeitafiles.duckdb" #-> CASO NAO DE DIRETO NO BANCO
    con = conectar_duckdb(path)
    if not con: return
    else:
      tables = list_db_tables(con)
      files = list_csv_files()
      list_all(tables, files)
      arq = selecionar_arquivos(files)
      if arq:
        pl = carregar_arquivos(con, arq)
        if pl:
            print("=" * 60)
            print(f"⚡ Arquivos carregados em memória:")
            for i in arq:
                print(f"- {i}\n")
            print("=" * 60)
            loop_interativo(pl)
        else: return
      else: return

def list_all(tables, files):
    if tables:
      try:
        for i,t in enumerate(tables): print(f"{i} - {t}\n")
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

def selecionar_arquivos(files):
    while True:
        print("=" * 60)
        print("📁 Selecione os arquivos CSV para carregar")
        print("🔢 Digite os números dos arquivos separados por vírgula")
        print("↩️ Digite \\exit para voltar ao menu anterior")
        print("*️⃣ Digite ENTER para selecionar todos os arquivos")
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

def carregar_arquivos(con, arquivos):
    try:
        for arq in arquivos:
          caminho = os.path.join(CSV_DIR, arq)
          nome_tabela = os.path.splitext(arq)[0]
          con.execute(
          f"CREATE OR REPLACE TEMP TABLE {nome_tabela} AS SELECT * FROM read_csv_auto('{caminho}')"
          ) # Trollando (depois arrumo, lol)
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
    print("\nDigite queries SQL (\\exit para sair, \\tables para listar tabelas)\n")
    print("=" * 65)
    while True:
        query = input("SQL> ").strip().lower()
        if query in ["\\exit", "exit", "quit"]:
            print("Saindo do módulo SQL...")
            break
        elif query in ["\\tables", ".tables"]:
            tabelas = con.execute("SHOW TABLES").fetchall()
            print("Tabelas carregadas:", [t[0] for t in tabelas])
        elif query:
            try:
                df = con.execute(query).df()
                print(df.head(20).to_string(index=False))
            except Exception as e:
                print(f"Erro: {e}")


