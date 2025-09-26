from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
XLSX_DIR = DATA_DIR / "xlsx"
CSV_DIR = DATA_DIR / "csv"

XLSX_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)