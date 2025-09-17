import os
import pandas as pd
import time
import chardet
from src.config import XLSX_DIR, CSV_DIR, BASE_DIR
from src.utils import *

def convert_menu():
    while True:
      print("=" * 38)
      print("-----------MODULO CONVERSAO-----------")
      print("=" * 38)
      print("Selecione o tipo de conversão:\n")
      print("0 - Voltar")
      print("1 - Converter xlsx para csv")
      print("2 - Converter encoding de arquivo csv")
      print("=" * 38)

      opcao = input("Escolha uma opção: ")

      if opcao == "0":
          clear()
          return
      elif opcao == "1":
        exec_convert_format()
        clear()
      elif opcao == "2":
        exec_convert_encoding()
        clear()
      else: 
        print("⚠️ Opção inválida, tente novamente!")
        time.sleep(1)
        clear()
 
def convert_xlsx_to_csv(input_path, output_dir, encoding="utf-8"):   
    try:
        xls = pd.ExcelFile(input_path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_file = f"{base_name}_{sheet_name}.csv"
            output_path = os.path.join(output_dir, output_file)
            os.makedirs(output_dir, exist_ok=True)
            df.to_csv(output_path, index=False, encoding=encoding)
            print(f"✅ Aba '{sheet_name}' convertida: {output_path}")
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado!")
        return
    except Exception as e:
        print(f"Erro ao converter: {e}")
        time.sleep(8)
        return

def convert_csv_encoding(input_path, output_path, target_encoding="utf-8"):
    try:
        df = pd.read_csv(input_path, encoding="utf-8", low_memory=False)
        df.to_csv(output_path, index=False, encoding=target_encoding)
        print(f"✅ Arquivo convertido para {target_encoding}: {output_path}")
    except Exception as e:
        print(f"❌ Erro ao converter: {e}")
        time.sleep(5)
        return

def detecta_encoding(input_path, sample_size=100000):
   try:
    with open(input_path, "rb") as f:
      raw_data = f.read(sample_size)
      result = chardet.detect(raw_data)
      encoding = result.get("encoding")
      confidence = result.get("confidence", 0)

    if encoding and confidence > 0.5:
      return encoding
    else:
      return None
   except Exception as e:
    print(f"❌ Erro ao detectar encoding: {e}")
    print("Voltando ao menu anterior...")
    time.sleep(2)
    return None

def escolha_valida(files, escolha):
    arquivo_selecionado = files[int(escolha)-1]
    input_path = os.path.join(CSV_DIR, arquivo_selecionado)
    original_encoding = detecta_encoding(input_path)
    if original_encoding == None:
       return
    else:
      encoding_info(original_encoding)
      print(f"\nNome do Arquivo: {arquivo_selecionado}\n")
      target_encoding = input("Digite o encoding de saída (ex: utf-8, latin1, cp1252): ").strip() or "utf-8"
      base_name = os.path.splitext(arquivo_selecionado)[0]
      output_file = f"{base_name}_{target_encoding}.csv"
      output_path = os.path.join(CSV_DIR, output_file)
      convert_csv_encoding(input_path, output_path, target_encoding)
      time.sleep(2)

def encoding_info(original_encoding):
   familias = {
    "ascii": "ASCII (básico: apenas inglês, compatível com quase todos os outros encodings)",
    "utf-8": "UTF-8 (universal: suporta todos os caracteres Unicode; inclui ASCII)",
    "latin-1": "Latin1 / ISO-8859-1 (idiomas da Europa Ocidental; próximo ao Windows-1252)",
    "windows-1252": "Windows-1252 (variação do Latin1 usada no Windows; traz símbolos extras como €, ™, —)",
    "utf-16": "UTF-16 (Unicode em 2 bytes; comum em arquivos do Windows e Excel, precisa de BOM para indicar ordem)",
    }
   info = familias.get(original_encoding.lower(), "Não tenho mais infos pra este encoding D:")
   return print(f"Encoding detectado: {original_encoding} Infos → {info}")

def exec_convert_encoding():
    files = list_csv_files()
    clear()
    print("=" * 38)
    for idx, f in enumerate(files, start=1): 
      print(f"{idx} - {f}")
    print("=" * 38)

    escolha = input("Escolha o arquivo para converter (ou 0 para voltar): ")

    if escolha == "0":
      return
    elif escolha.isdigit() and 1 <= int(escolha) <= len(files):
      escolha_valida(files, escolha)
    else:
      print("⚠️ Opção inválida, tente novamente!")
      time.sleep(1)    

def exec_convert_format():
    files = list_xlsx_files()
    clear()
    print("=" * 38)
    for idx, f in enumerate(files, start=1):
      print(f"{idx} - {f}")
    print("=" * 38)

    opcao = input("Escolha o arquivo para converter (ou 0 para voltar): ")
    if opcao == "0":
      return
    elif opcao.isdigit() and 1 <= int(opcao) <= len(files):
      arquivo_selecionado = files[int(opcao)-1]
      input_path = os.path.join(XLSX_DIR, arquivo_selecionado)
      output_file = os.path.splitext(arquivo_selecionado)[0] + ".csv"
      output_path = CSV_DIR
      convert_xlsx_to_csv(input_path, output_path)
      time.sleep(1.5)
    else:
      print("=" * 38)
      print("\n⚠️ Opção inválida, tente novamente!")
      time.sleep(1)
      return

