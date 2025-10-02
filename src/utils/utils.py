# src/utils.py
import os
from src.config.config import CSV_DIR, XLSX_DIR

#Busca os arquivos.
def get_files(directory: str, extension: str) -> list[str]:

    return [
        f for f in os.listdir(directory) 
        if f.lower().endswith(extension.lower())
    ]


def get_csv_files() -> list[str]:
    return get_files(CSV_DIR, ".csv")

def get_xlsx_files() -> list[str]:
    return get_files(XLSX_DIR, ".xlsx")

#Lista as tabelas do database.
def get_db_tables(con):
    try:
        tables = con.execute("SHOW TABLES").fetchall()
        if not [t[0] for t in tables]:
            return []
        else:
          return [t[0] for t in tables]
    except Exception as e:
        print(f"Erro ao listar tabelas no banco.{e}")
        return None