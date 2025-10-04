import os
import pandas as pd
from pathlib import Path
import csv
import time
from src.utils.utils import *
from src.utils.menu import *
from src.config.config import *


def split_menu():
    clear()
    title = ":crossed_swords: MODULO SPLITTER :crossed_swords:"
    com = [
      "Digite o número dos arquivos separados por vírgula",
      "Digite \\exit para voltar ao menu anterior",
      "Digite ENTER para selecionar todos os arquivos"
    ]
    print_header(title, com, M_MAIN, M_CONFIG)
    files = list_files_to_split()

    selected = select_file(files)
    if selected is None:
        return
    chunk = set_chunk()
    if chunk is None:
        return
    split_csv(selected, chunk)
            
def set_chunk():
    while True:
        print("\nDefina a quantidade de linhas por arquivo")
        print("Digite ENTER para quantidade default (o default é 100.000 linhas).")
        print("Digite \\exit para voltar ao menu anterior\n")
        lines_per_file = input("Pelo amor de deus digite apenas numeros aqui: ")
        if lines_per_file == "\\exit":
            return None
        if not lines_per_file:
            return 100000
        validate_input = lines_per_file.replace(".","").replace(",","")
        if validate_input.isdigit():
            try:
                chunk = int(validate_input)
                return chunk
            except ValueError:
                print(f"⚠️ Erro na conversão: {ValueError}")
                continue           
        else: 
            print("\n⚠️ Are you kidding me?")
            time.sleep(1)

def list_files_to_split():
    files = get_csv_files()
    if not files:
        warn("Nenhum arquivo csv encontrado")
        time.sleep(1.5)
        return
    if files:
        print_menu(":file_folder: Selecione o(s) arquivo(s) da /csv/ para dividir:", files, M_MAIN)
        return files
    else:
        return

def select_file(files):
    while True:
        escolha = input("\n>").strip()

        if escolha in ("\\exit", "exit", "00"):
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

def detect_separator(filepath, sample_size=1024, fallback_sep=','):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sample = f.read(sample_size)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)            
            delimiter, quotechar = dialect.delimiter, dialect.quotechar
            kwargs_read, kwarg_write = handle_args(quotechar, delimiter)
            return kwargs_read, kwarg_write
    except Exception as e:
        print(f"⚠️ Erro ao detectar separador, usando padrão ('{fallback_sep}'): {e}")
        return {"sep": fallback_sep, "dtype": str, "low_memory": False}, {
          "index": False, "sep": fallback_sep, "quoting": csv.QUOTE_NONE
        }
        
def handle_args(quotechar, delimiter):
       
    if quotechar is None:
        kwargs_write = {
          "index": False,
          "sep": delimiter,
          "quoting": csv.QUOTE_NONE # LEMBRAR! testar aumentar o sample do sniffer pra detectar exceções
        }
        kwargs_read = {
          "sep": delimiter,
          "dtype": str,
          "low_memory": False
        }
    else:
        kwargs_write = {
        "index": False,
        "sep": delimiter,
        "quotechar": quotechar,
        "quoting": csv.QUOTE_ALL
      }
        kwargs_read = {
          "sep": delimiter,
          "quotechar": quotechar,
          "dtype": str,
          "low_memory": False
        }
    return kwargs_read, kwargs_write

def validate_chunk(chunk: int) -> int:
    try:
        lines_per_file = int(chunk)
        if lines_per_file <= 0:
            raise ValueError("chunk deve ser > 0")
        return lines_per_file
    except Exception as e:
        raise ValueError(f"Parâmetro 'chunk' inválido: {e}")

def prepare_output_dir(base_dir=CSV_DIR) -> Path:
    output_dir = Path(base_dir) / "splits"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def normalize_filepaths(filepaths, base_dir=CSV_DIR) -> list[Path]:
    if isinstance(filepaths, (str, Path)):
        filepaths = [filepaths]

    normalized = []
    for fp in filepaths:
        fp = Path(fp)
        if not fp.is_absolute():
            fp = Path(base_dir) / fp
        if fp.exists():
            normalized.append(fp)
        else:
            print(f"⚠️ Arquivo não encontrado, pulando: {fp}")
    return normalized

def process_file(fp: Path, lines_per_file: int, output_dir: Path):
    filename = fp.stem
    print(f"📂 Processando: {fp}")

    try:
        kwargs_read, kwargs_write = detect_separator(fp)
        
        for i, chunk_df in enumerate(pd.read_csv(fp, chunksize=lines_per_file, **kwargs_read)):
            out_path = output_dir / f"{filename}_part{i+1}.csv"
            chunk_df.to_csv(out_path, **kwargs_write)
            print(f"[OK] Arquivo gerado: {out_path}")

    except Exception as e:
        print(f"Erro ao processar {fp}: {e}")
        time.sleep(200)

    finally:
        print("Split finalizado com sucesso!")
        print("Retornando ao menu principal.")
        time.sleep(2)

def split_csv(filepaths, chunk):
    lines_per_file = validate_chunk(chunk)
    output_dir = prepare_output_dir()
    filepaths = normalize_filepaths(filepaths)

    for fp in filepaths:
        process_file(fp, lines_per_file, output_dir)
        return

