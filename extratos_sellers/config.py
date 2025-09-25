from pathlib import Path

# diretorios
RAIZ = Path(__file__).parent.parent  # extratos-sellers/
DIR_DATA = RAIZ / "data"
DIR_SCRIPTS = RAIZ / "extratos_sellers"
DIR_OUTPUT = DIR_DATA / "output"
DIR_TEMPFILES = DIR_DATA / "temp_files"

# arquivos fonte
ARQ_CONTASARECEBER = next((DIR_DATA / "input").glob("*.xls"))
ARQ_COMISSOES = DIR_DATA / "comissoes.xlsx"
ARQ_APPEL = DIR_DATA / "appel.xlsx"
ARQ_DATALAN = DIR_DATA / "datalan.xlsx"

# mapeamento de colunas
COLUNAS = {
    "IDENTIFICADOR_CLIENTE": "Identificador do cliente",
    "NOME_CLIENTE": "Nome do cliente",
    "DATA_COMPETENCIA": "Data de competência",
    "DATA_VENCIMENTO": "Data de vencimento",
    "VALOR_ORIGINAL_PARCELA": "Valor original da parcela (R$)",
    "VALOR_RECEBIDO_PARCELA": "Valor recebido da parcela (R$)",
    "DATA_ULTIMO_PAGAMENTO": "Data do último pagamento",
}

COLUNAS_CRIADAS = {
    "NOME_RESSELLER": "nome_resseller",
    "SELLERS": "SELLERS",
    "RESSELLERS": "RESSELLERS",
    "COMISSAO": "COMISSÃO",
    "TOTAL_REPASSE": "TOTAL DO REPASSE (R$)",
}
