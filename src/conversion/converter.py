import os
import pandas as pd
import time
import chardet
from src.config.config import XLSX_DIR, CSV_DIR, BASE_DIR
from src.utils.utils import *

def convert_menu():
    while True:
        clear()
        largura = 65
        print("=" * largura)
        print("🔄 MÓDULO DE CONVERSÃO 🔄".center(largura))
        print("=" * largura)
        print("Selecione o tipo de conversão:\n".center(largura))
        print("0 - Voltar".ljust(largura))
        print("1 - Converter XLSX para CSV".ljust(largura))
        print("2 - Converter encoding de arquivo CSV".ljust(largura))
        print("=" * largura)


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
    print(f"Encoding detectado: {encoding}\nInfos → {info}")

def handle_encoding_choice(files: list[str], escolha: str) -> None:
    arquivo = files[int(escolha) - 1]
    input_path = CSV_DIR / arquivo
    largura = 65

    original_encoding = detect_encoding(input_path)
    if not original_encoding:
        print("Erro ao detectar encoding!")
        return

    clear()
    print("=" * largura)
    print("Informações sobre o arquivo".center(largura))
    print(f"\nNome do Arquivo → {arquivo}\n")
    print("=" * largura)
    encoding_info(original_encoding)
    print("=" * largura)

    base_name = Path(arquivo).stem
    output_file = f"{base_name}_UTF8.csv"
    output_path = CSV_DIR / output_file

    convert_encoding_file(input_path, output_path, original_encoding)
    time.sleep(1)

def exec_convert_encoding():
    files = list_csv_files()
    clear()
    largura = 65

    if not files:
        print("=" * largura)
        print("⚠️ Nenhum arquivo CSV encontrado!".center(largura))
        print("=" * largura)
        time.sleep(1.5)
        return

    print("=" * largura)
    print("🌐 CONVERSÃO DE ENCODING DE CSV 🌐".center(largura))
    print("=" * largura)
    print("⚠️ Atualmente só posso converter pra UTF-8 ⚠️".center(largura))
    print()

    for idx, f in enumerate(files, start=1):
        print(f"{idx} 📄 {f}".ljust(largura))

    print("=" * largura)
    escolha = input("Escolha o arquivo para converter (ou 0 para voltar): ")

    if escolha == "0":
        return
    elif escolha.isdigit() and 1 <= int(escolha) <= len(files):
        handle_encoding_choice(files, escolha)
        print("\n✅ Conversão concluída com sucesso!")
        time.sleep(1)
    else:
        print("=" * largura)
        print("⚠️ Opção inválida, tente novamente!".center(largura))
        print("=" * largura)
        time.sleep(1)

def exec_convert_format():
    files = list_xlsx_files()
    clear()
    largura = 65

    if not files:
        print("=" * largura)
        print("⚠️  Nenhum arquivo XLSX encontrado!".center(largura))
        print("=" * largura)
        time.sleep(1.5)
        return

    print("=" * largura)
    print("📈 ARQUIVOS XLSX DISPONÍVEIS 📈".center(largura))
    print("=" * largura)

    for idx, f in enumerate(files, start=1):
        print(f"{idx} 📑 {f}".ljust(largura))

    print("=" * largura)
    opcao = input("Escolha o arquivo para converter (ou 0 para voltar): ")

    if opcao == "0":
        return

    elif opcao.isdigit() and 1 <= int(opcao) <= len(files):
        arquivo_selecionado = files[int(opcao) - 1]

        input_path = XLSX_DIR / arquivo_selecionado
        output_file = Path(arquivo_selecionado).stem + ".csv"
        output_path = CSV_DIR / output_file

        convert_xlsx_to_csv(input_path, output_path)
        print(f"\n✅ Arquivo convertido com sucesso: {output_file}")
        time.sleep(1.5)

    else:
        print("=" * largura)
        print("⚠️  Opção inválida, tente novamente!".center(largura))
        print("=" * largura)
        time.sleep(1)
        return
    
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