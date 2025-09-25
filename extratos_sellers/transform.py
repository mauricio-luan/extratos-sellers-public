import re
import numpy as np
import pandas as pd
from .config import (
    COLUNAS,
    COLUNAS_CRIADAS,
    DIR_TEMPFILES,
)


def clean_dataframes(
    contas_a_receber: pd.DataFrame, comissoes: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Realiza a limpeza e padronização dos DataFrames de contas a receber e comissões.
    Extrai e cria a coluna de 'nome_resseller' a partir do nome do cliente, aplica
    formatações (maiúsculas e remoção de espaços) nas colunas de interesse e salva
    uma versão intermediária do DataFrame de contas a receber para depuração.
    """

    contas_a_receber[COLUNAS_CRIADAS["NOME_RESSELLER"]] = contas_a_receber[
        COLUNAS["NOME_CLIENTE"]
    ].apply(extract_resseller_name)

    contas_a_receber[COLUNAS["IDENTIFICADOR_CLIENTE"]] = (
        contas_a_receber[COLUNAS["IDENTIFICADOR_CLIENTE"]]
        .astype(str)
        .str.zfill(14)  # garante os 14 digitos do cnpj. colocando 0 a esquerda
        .str.strip()
    )

    contas_a_receber[COLUNAS_CRIADAS["NOME_RESSELLER"]] = (
        contas_a_receber[COLUNAS_CRIADAS["NOME_RESSELLER"]].str.upper().str.strip()
    )

    comissoes[COLUNAS_CRIADAS["RESSELLERS"]] = (
        comissoes[COLUNAS_CRIADAS["RESSELLERS"]].str.upper().str.strip()
    )

    contas_a_receber.to_excel(
        DIR_TEMPFILES / "1-contas_a_receber_com_resselers.xlsx", index=False
    )

    return contas_a_receber, comissoes


def merge_dataframes(
    contas_a_receber: pd.DataFrame, comissoes: pd.DataFrame
) -> pd.DataFrame:
    """
    Realiza o merge entre os DataFrames de contas a receber e comissões, vinculando
    cada 'resseller' ao respectivo 'seller' e à taxa de comissão. Mantém todas as
    linhas de contas a receber, adicionando dados de comissões somente quando há
    correspondência, e gera uma versão intermediária do resultado para depuração.
    """

    # Traz para a contas_a_receber as colunas RESSELLERS, SELLERS e COMISSAO de comissoes
    # a partir do merge entre a coluna 'nome_resseller' e a coluna 'RESSELLERS'.
    # Mantém todas linhas de contas_a_receber e só adiciona os dados de comissoes quando
    # encontra correspondência.
    contas_a_receber = contas_a_receber.merge(
        comissoes[
            [
                COLUNAS_CRIADAS["RESSELLERS"],
                COLUNAS_CRIADAS["SELLERS"],
                COLUNAS_CRIADAS["COMISSAO"],
            ]
        ],
        left_on=COLUNAS_CRIADAS["NOME_RESSELLER"],
        right_on=COLUNAS_CRIADAS["RESSELLERS"],
        how="left",
    )

    contas_a_receber.to_excel(
        DIR_TEMPFILES / "2-contas_a_receber_reseller_comissoes.xlsx", index=False
    )

    return contas_a_receber


def calculate_payout(contas_a_receber: pd.DataFrame) -> pd.DataFrame:
    """
    Finaliza o DataFrame de contas a receber após o merge, calculando a coluna de
    repasse ('TOTAL_REPASSE') a partir do valor da parcela e da taxa de comissão,
    truncado em duas casas decimais. Em seguida, mantém apenas as linhas com sellers
    válidos (não nulos e diferentes de 'SEM SELLER') e salva o resultado em arquivo
    para depuração.
    """

    comissao = (
        contas_a_receber[COLUNAS["VALOR_RECEBIDO_PARCELA"]]
        * contas_a_receber[COLUNAS_CRIADAS["COMISSAO"]]
    )
    contas_a_receber[COLUNAS_CRIADAS["TOTAL_REPASSE"]] = np.trunc(comissao * 100) / 100

    # filtra as linhas com sellers validos
    seller_validos = (contas_a_receber[COLUNAS_CRIADAS["SELLERS"]].notna()) & (
        contas_a_receber[COLUNAS_CRIADAS["SELLERS"]] != "SEM SELLER"
    )
    contas_a_receber = contas_a_receber[seller_validos]

    contas_a_receber.to_excel(
        DIR_TEMPFILES / "3-contas_a_receber_final.xlsx", index=False
    )
    return contas_a_receber


def extract_resseller_name(nome_cliente) -> str | None:
    """Extrai o nome do resseler de dentro da celula, a partir do nome do cliente."""

    resultado = re.search(r"\((.*?)\)", str(nome_cliente))
    if resultado:
        return resultado.group(1).strip()
    return None


def transform(contas_a_receber: pd.DataFrame, comissoes: pd.DataFrame) -> pd.DataFrame:
    """Orquestra funções de transform dos Dataframes."""

    try:
        df_contas_a_receber, df_comissoes = clean_dataframes(
            contas_a_receber, comissoes
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao limpar dataframes: {e}") from e

    try:
        contas_a_receber_merged = merge_dataframes(df_contas_a_receber, df_comissoes)
    except Exception as e:
        raise RuntimeError(f"Erro ao mergear dataframes: {e}") from e

    try:
        contas_a_receber_final = calculate_payout(contas_a_receber_merged)
    except Exception as e:
        raise RuntimeError(f"Erro ao calcular payout: {e}") from e

    return contas_a_receber_final
