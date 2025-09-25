from pathlib import Path
from openpyxl.utils.exceptions import InvalidFileException
import pandas as pd
from .config import (
    ARQ_CONTASARECEBER,
    ARQ_COMISSOES,
    COLUNAS,
)


def load_file(file_path: Path, cols: list = None) -> pd.DataFrame:
    """
    Carrega um arquivo Excel em um DataFrame, mantendo apenas as colunas especificadas
    (se fornecidas), ajustando o separador decimal para vírgula e removendo espaços
    extras dos nomes das colunas.
    """

    df = pd.read_excel(file_path, usecols=cols, decimal=",")
    df.columns = df.columns.str.strip()
    return df


def load() -> tuple[pd.DataFrame]:
    """
    Carrega e retorna os arquivos de contas a receber (com colunas específicas) e de
    comissões como DataFrames. Utiliza a função `load_file` para realizar a leitura
    dos arquivos.
    """

    try:
        df_contas_a_receber = load_file(ARQ_CONTASARECEBER, COLUNAS.values())
        df_comissoes = load_file(ARQ_COMISSOES)

        return df_contas_a_receber, df_comissoes

    except FileNotFoundError as e:
        raise ValueError(f"Arquivo não encontrado. Detalhes: {e}") from e

    except ValueError as e:
        raise ValueError(f"Arquivo vazio: {e}") from e

    except InvalidFileException as e:
        raise ValueError(f"Tipo de arquivo inválido: {e}") from e

    except Exception as e:
        raise ValueError(f"Erro ao carregar planilhas: {e}") from e


if __name__ == "__main__":
    load()
