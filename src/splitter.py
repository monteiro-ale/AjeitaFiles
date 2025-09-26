import os
import pandas as pd
from pathlib import Path
import csv
import time
from src.utils import *
from src.config import *


def split_menu():
    clear()
    largura = 65
    title = "⚔️ MODULO SPLITTER ⚔️"

    print("=" * largura)
    print(title.center(largura))
    print("=" * largura)
    files = list_files()
    if files:
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
            return
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


def list_files():
    files = list_csv_files()
    if files:
        print("=" * 65)
        print("\n⚔️ Arquivos disponíveis para splittar: (📂 Folder csv):\n")
        for idx, f in enumerate(files, start=1): 
            print(f"{idx} - {f}\n")
        return files
    else:
        return

def select_file(files):
    while True:
        print("=" * 65)
        print("📁 Selecione os arquivos .CSV para splittar")
        print("🔢 Digite os números dos arquivos separados por vírgula")
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


def split_csv(filepaths, chunk):
    try:
        lines_per_file = int(chunk)
        if lines_per_file <= 0:
            raise ValueError("chunk deve ser > 0")
    except Exception as e:
        raise ValueError(f"Parâmetro 'chunk' inválido: {e}")

    output_dir = Path(CSV_DIR) / "splits"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # normalizar filepaths para lista
    if isinstance(filepaths, (str, Path)):
        filepaths = [filepaths]

    for filepath in filepaths:
        fp = Path(filepath)
        if not fp.is_absolute():
            fp = Path(CSV_DIR) / fp

        if not fp.exists():
            print(f"⚠️ Arquivo não encontrado, pulando: {fp}")
            continue

        filename = fp.stem
        print(f"📂 Processando: {fp}")

        try:
            # Detecta o separador antes de ler o arquivo
            kwargs_read, kwargs_write = detect_separator(fp)
            
            for i, chunk_df in enumerate(pd.read_csv(fp, chunksize=lines_per_file, **kwargs_read)):
                out_path = output_dir / f"{filename}_part{i+1}.csv"

                chunk_df.to_csv(out_path, **kwargs_write)
                print(f"[OK] Arquivo gerado: {out_path}")
                #time.sleep(1)
        except Exception as e:
            print(f"Erro ao processar {fp}: {e}")
            time.sleep(200)

        finally: 
            print("Split finalizado com sucesso!")
            print("Retornando ao menu principal.")
            time.sleep(2)
            return
        
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

