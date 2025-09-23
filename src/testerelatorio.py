import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

def gerar_relatorio(df: pd.DataFrame, colunas_chave: list[str] | None = None):
    table = Table(title="📊 Relatório do Arquivo")

    # Cabeçalhos da tabela de resumo
    table.add_column("Característica", style="cyan", no_wrap=True)
    table.add_column("Valor", style="magenta")

    # --- Características básicas
    table.add_row("📑 Nº de colunas", str(df.shape[1]))
    table.add_row("📊 Nº de linhas", str(df.shape[0]))

    # --- Colunas-chave
    if colunas_chave:
        table.add_row("🔑 Colunas-chave", ", ".join(colunas_chave))

        # Validação de duplicatas
        duplicatas = df.duplicated(subset=colunas_chave).sum()
        table.add_row("🌀 Linhas duplicadas", str(duplicatas))
    else:
        table.add_row("🔑 Colunas-chave", "Não informado")
        table.add_row("🌀 Linhas duplicadas", "0 (chaves não definidas)")

    # --- Valores nulos
    nulos = df.isnull().sum()
    nulos_percent = (nulos / len(df) * 100).round(2)

    null_summary = ", ".join(
        f"{col}: {pct}%" for col, pct in nulos_percent.items() if pct > 0
    ) or "Nenhum valor nulo encontrado"

    table.add_row("🕳️ Valores nulos (%)", null_summary)

    # --- Tipos de dados
    tipos = ", ".join(f"{col}: {dtype}" for col, dtype in df.dtypes.items())
    table.add_row("🧩 Tipos de dados", tipos)

    # --- Colunas constantes
    constantes = df.nunique()
    constantes = constantes[constantes == 1]  # pega só colunas com 1 valor único
    if not constantes.empty:
        const_summary = ", ".join(
            f"{col}: {df[col].iloc[0]!r}" for col in constantes.index
        )
    else:
        const_summary = "Nenhuma coluna constante encontrada"
    table.add_row("📌 Colunas constantes", const_summary)

    # --- Cardinalidade por coluna
    cardinalidade = df.nunique()
    card_summary = ", ".join(
        f"{col}: {val} ({round(val/len(df)*100, 2)}%)"
        for col, val in cardinalidade.items()
    )
    table.add_row("🔢 Cardinalidade", card_summary)


    console.print(table)


# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo com CSV
    df = pd.DataFrame({
        "id": [1, 2, 2, 3, None],
        "nome": ["Ana", "Beto", "Beto", "Carla", "Ana"],
        "idade": [23, 35, 35, None, 23]
    })

    # Usuário informa colunas-chave
    chaves = input("Digite as colunas-chave (separadas por vírgula) ou Enter se não houver: ")
    colunas_chave = [c.strip() for c in chaves.split(",")] if chaves else None

    gerar_relatorio(df, colunas_chave)
