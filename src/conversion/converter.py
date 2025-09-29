import os
import pandas as pd
import time
import chardet
from rich import print
from src.config.config import *
from src.utils.utils import *
from src.utils.menu import *

def convert_menu():
    while True:
        clear()
        opt = [
            ":fast_reverse_button: Voltar ao menu anterior",
            ":counterclockwise_arrows_button: Converter XLSX para CSV",
            ":counterclockwise_arrows_button: Converter encoding de arquivo CSV"
        ]
        
        print_menu("🔄 MÓDULO DE CONVERSÃO 🔄", opt)

        opcao = input("Escolha uma opção: ")

        if opcao in("\\exit", "0"):
            clear()
            return
        elif opcao == "2":
            exec_convert_format()
            clear()
        elif opcao == "3":
            exec_convert_encoding()
            clear()
        else: 
            warn("Opção inválida, tente novamente!", 1)
            clear()

def detect_encoding(input_path: Path, sample_size=100_000) -> str | None:
    try:
        with open(input_path, "rb") as f:
            raw_data = f.read(sample_size)
            result = chardet.detect(raw_data)
            encoding = result.get("encoding")
            confidence = result.get("confidence", 0)

        return encoding if encoding and confidence > 0.5 else None

    except Exception as e:
        print(f"❌ Erro ao detectar encoding: {e}")
        time.sleep(2)
        return None

def convert_encoding_file(input_path: Path, output_path: Path, detected_encoding: str) -> bool:
    try:
        with open(input_path, "r", encoding=detected_encoding, errors="replace") as fin:
            content = fin.read()

        with open(output_path, "w", encoding="utf-8", newline="") as fout:
            fout.write(content)

        print(f"✅ Arquivo convertido para UTF-8: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Erro ao converter: {e}")
        time.sleep(2)
        return False

def encoding_info(encoding: str) -> None:
    familias = {
        "ascii": "ASCII (básico: apenas inglês, compatível com quase todos os outros encodings)",
        "utf-8": "UTF-8 (universal: suporta todos os caracteres Unicode; inclui ASCII)",
        "latin-1": "Latin1 / ISO-8859-1 (idiomas da Europa Ocidental; próximo ao Windows-1252)",
        "windows-1252": "Windows-1252 (variação do Latin1 usada no Windows; traz símbolos extras como €, ™, —)",
        "utf-16": "UTF-16 (Unicode em 2 bytes; comum em arquivos do Windows e Excel, precisa de BOM para indicar ordem)",
    }
    info = familias.get(encoding.lower(), "Não tenho mais infos pra este encoding D:")
    return info

def handle_encoding_choice(files: list[str], escolha: str) -> None:
    arquivo = files[int(escolha) - 1]
    input_path = CSV_DIR / arquivo

    original_encoding = detect_encoding(input_path)
    if not original_encoding:
        error("Erro ao detectar encoding!")
        return

    clear()
    enc_info = encoding_info(original_encoding)
    print("[bold yellow]Informações sobre o arquivo[/bold yellow]\n")
    print(f"Nome do Arquivo → {arquivo}")
    print(f"Encoding de entrada → {original_encoding}\n")
    info(enc_info)
    print("\nPressione [bold yellow]ENTER[/bold yellow] para converter.")
    input()

    base_name = Path(arquivo).stem
    output_file = f"{base_name}_UTF8.csv"
    output_path = CSV_DIR / output_file

    convert_encoding_file(input_path, output_path, original_encoding)
    time.sleep(1)

def exec_convert_encoding():
    files = get_csv_files()
    if not files:
        warn("Nenhum arquivo CSV encontrado!", 1.5)
        return
    else:
      clear()
      largura = 65

      print_menu("🌐 CONVERSÃO DE ENCODING DE CSV 🌐", files)
      print("⚠️ Atualmente só posso converter pra UTF-8 ⚠️".center(largura))
      print()
      escolha = input("Escolha o arquivo para converter (ou \\exit para voltar): ")

      if escolha in ("\\exit", "exit", "0"):
          return
      elif escolha.isdigit() and 1 <= int(escolha) <= len(files):
          handle_encoding_choice(files, escolha)
          print("\n✅ Conversão concluída com sucesso!")
          time.sleep(1)
      else:
          warn("Opção inválida, tente novamente!", 1)

def exec_convert_format():
    files = get_xlsx_files()
    clear()

    if not files:
        warn("Nenhum arquivo XLSX encontrado!", 1.5)
        return

    print_menu("📈 ARQUIVOS XLSX DISPONÍVEIS 📈", files)
    opcao = input("Escolha o arquivo para converter (ou \\exit para voltar): ")

    if opcao in ("\\exit", "exit", "0"):
        return

    elif opcao.isdigit() and 1 <= int(opcao) <= len(files):
        arquivo_selecionado = files[int(opcao) - 1]

        args, output_file = prepare_path(arquivo_selecionado)

        convert_xlsx_to_csv(**args)
        print(f"\n✅ Arquivo convertido com sucesso: {output_file}")
        time.sleep(1.5)

    else:
        warn("Opção inválida, tente novamente!", 1)
        return

def prepare_path(file):   
    output_file = Path(file).stem + ".csv"
    args = {
    "input_path": XLSX_DIR / file,
    "output_path": CSV_DIR 
    }

    return args, output_file

def convert_xlsx_to_csv(input_path, output_path, encoding="utf-8"): 
    try:
        xls = pd.ExcelFile(input_path)
        base_name = Path(input_path).stem
        out_dir = Path(output_path) / base_name
        out_dir.mkdir(parents=True, exist_ok=True)

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            output_file = out_dir / f"{base_name}_{sheet_name}.csv"
            df.to_csv(output_file, index=False, encoding=encoding)
            print(f"✅ Aba '{sheet_name}' convertida: {output_path}")

    except FileNotFoundError:
        error("Arquivo de entrada não encontrado!")
        return
    except Exception as e:
        error(f"Erro ao converter: {e}")
        time.sleep(8)
        return

