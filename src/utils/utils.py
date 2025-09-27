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
    
