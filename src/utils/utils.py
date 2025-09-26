import os
import time
from src.config.config import *

def clear():
  return os.system("cls")

#Lembrar de mais algumas outras uteis 

def list_csv_files():
    #Lista os csv's da folder csv.
    files = [f for f in os.listdir(CSV_DIR) if f.lower().endswith(".csv")]
    if not files:
      print("⚠️ Nenhum arquivo CSV encontrado na pasta data/csv.")
      time.sleep(5)
      return
    else:
      return files
    
def list_xlsx_files():
    #Lista arquivos XLSX da pasta data/xlsx
    files = [f for f in os.listdir(XLSX_DIR) if f.lower().endswith(".xlsx")]
    if not files:
      print("⚠️ Nenhum arquivo XLSX encontrado na pasta data/xlsx")
      time.sleep(5)
      return
    else:
      return files
    
def valida_escolha_sn(escolha): #Tem que traduzir umas escolhas pra essa se encaixar.
    if escolha.lower() in ("s", "n"):
      return True
    else: 
      return False

def valida_escolha_number(escolhas, min_val=1, max_val=None): #Essa tem que criar o range pra passar por parâmetro.
    if not escolhas:  # lista vazia = ENTER = nenhum escolhido
        return []

    try:
        indices = []
        for parte in escolhas:
            if not parte.isdigit():
                print(f"⚠️ Valor inválido: {parte}")
                return None

            num = int(parte)
            if num < min_val or (max_val and num > max_val):
                print(f"⚠️ Número fora do intervalo permitido: {num}")
                return None

            indices.append(num)

        return indices
    except Exception as e:
        print(f"⚠️ Erro ao validar: {e}")
        return None

def importar_para_banco(con, arquivos):
    for arq in arquivos:
        caminho = os.path.join(CSV_DIR, arq)
        nome_tabela = os.path.splitext(arq)[0]
        try:
            query = f"""CREATE TABLE {nome_tabela} AS SELECT * FROM read_csv_auto('{caminho}', sample_size=-1)"""
            con.execute(query)
            print(f"[OK] Tabela persistida: {nome_tabela}")
        except Exception as e:
            print(f"Erro ao importar {arq}: {e}")

def carregar_in_memory(con, arquivos):
    aliases = {}
    for idx, arq in enumerate(arquivos, start=1):
        caminho = os.path.join(CSV_DIR, arq)
        alias = f"t{idx}"
        try:
            query = f"""CREATE TEMP TABLE {alias} AS SELECT * FROM read_csv_auto('{caminho}', sample_size=-1)"""
            con.execute(query)
            aliases[alias] = arq
            print(f"[TEMP] {arq} carregado como {alias}")
        except Exception as e:
            print(f"Erro ao carregar {arq}: {e}")
    return aliases