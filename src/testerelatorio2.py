import duckdb
from src.config import *
from src.utils import *


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

# def exec_relatorio(selected):
#     filepaths = []
#     for file in selected:
#         f = str(file)
#         filepaths.append(CSV_DIR / f)
#         diagnostico_duckdb(filepaths, f)

def exec_relatorio(selected):
    for file in selected:
        filepath = CSV_DIR / file
        table_name = os.path.splitext(file)[0]  # tira o .csv
        diagnostico_duckdb(filepath, table_name)


# def diagnostico_duckdb(filepath, table_name="tabela"):
#     con = duckdb.connect()

#       # Carrega o CSV como uma tabela
#     con.execute(f"""
#         CREATE OR REPLACE TABLE {table_name} AS 
#         SELECT * FROM read_csv_auto('{filepath}', header=True, SAMPLE_SIZE=-1)
#     """)

#     print("📂 Arquivo carregado com sucesso!\n")

#     # Número de linhas e colunas
#     shape = con.execute(f"SELECT COUNT(*) AS linhas FROM {table_name}").fetchone()[0]
#     cols = con.execute(f"PRAGMA table_info({table_name})").fetchall()
#     print(f"Linhas: {shape:,}")
#     print(f"Colunas: {len(cols)}\n")

#     # Colunas constantes
#     print("🔹 Colunas constantes (mesmo valor em 100% das linhas):")
#     const_cols = con.execute(f"""
#         SELECT column_name, COUNT(DISTINCT {table_name}.column_name) AS distincts
#         FROM pragma_table_info('{table_name}') 
#         JOIN {table_name} ON TRUE
#         GROUP BY column_name
#         HAVING distincts = 1
#     """).fetchall()
#     if const_cols:
#         for c in const_cols:
#           print(f" - {c[0]}")
#     else:
#         print("Nenhuma coluna constante encontrada.")
#     print()

#     # Cardinalidade por coluna
#     print("🔹 Cardinalidade (nº de valores únicos por coluna):")
#     for c in cols:
#         col = c[1]
#         nuniq = con.execute(f"SELECT COUNT(DISTINCT {col}) FROM {table_name}").fetchone()[0]
#         print(f" - {col}: {nuniq:,}")
#     print()

#     # Valores nulos por coluna
#     print("🔹 Nulos por coluna:")
#     for c in cols:
#         col = c[1]
#         nnulos = con.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {col} IS NULL").fetchone()[0]
#         print(f" - {col}: {nnulos:,}")
#     print()

#     con.close()

def diagnostico_duckdb(filepath, table_name="tabela"):
    con = duckdb.connect()

    # Carrega o CSV como uma tabela
    con.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{str(filepath)}', header=True, SAMPLE_SIZE=-1)
    """)

    print("📂 Arquivo carregado com sucesso!\n")

    # Número de linhas e colunas
    shape = con.execute(f"SELECT COUNT(*) AS linhas FROM {table_name}").fetchone()[0]
    cols = con.execute(f"PRAGMA table_info({table_name})").fetchall()
    print(f"Linhas: {shape:,}")
    print(f"Colunas: {len(cols)}\n")

    # Colunas constantes
    print("🔹 Colunas constantes (mesmo valor em 100% das linhas):")
    constantes = []
    for c in cols:
        col = c[1]
        distincts = con.execute(f'SELECT COUNT(DISTINCT "{col}") FROM "{table_name}"').fetchone()[0]
        if distincts == 1:
            constantes.append(col)

    if constantes:
        for col in constantes:
            print(f" - {col}")
    else:
        print("Nenhuma coluna constante encontrada.")
    print()

    # Cardinalidade por coluna
    print("🔹 Cardinalidade (nº de valores únicos por coluna):")
    for c in cols:
        col = c[1]
        nuniq = con.execute(f'SELECT COUNT(DISTINCT "{col}") FROM "{table_name}"').fetchone()[0]
        print(f" - {col}: {nuniq:,}")
    print()

    # Valores nulos por coluna
    print("🔹 Nulos por coluna:")
    for c in cols:
        col = c[1]
        nnulos = con.execute(f'SELECT COUNT(*) FROM "{table_name}" WHERE "{col}" IS NULL').fetchone()[0]
        print(f" - {col}: {nnulos:,}")
    print()
    time.sleep(10)

    con.close()


