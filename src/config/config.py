from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
XLSX_DIR = DATA_DIR / "xlsx"
CSV_DIR = DATA_DIR / "csv"

XLSX_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)


M_MAIN = "#FFD700"  # Ouro
M_CONVERTER = "#9ed0ae"  # Verde
M_REPORT = "#99C8F2"  # Azul
M_CONFIG    = "#A9A9A9"  # Cinza
M_DUCK = "#6495ED"