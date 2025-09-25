import pandas as pd
from .config import COLUNAS_CRIADAS, DIR_OUTPUT


def save(contas_a_receber: pd.DataFrame) -> None:
    """
    Salva relatórios individuais em Excel a partir do DataFrame final de contas a
    receber.
    Remove colunas auxiliares, agrupa os dados por seller e, para cada grupo, cria um
    arquivo .xlsx contendo as linhas do seller e uma linha extra com o total de repasses.
    """

    try:
        DIR_OUTPUT.mkdir(parents=True, exist_ok=True)

        contas_a_receber = contas_a_receber.drop(
            columns=[
                COLUNAS_CRIADAS["RESSELLERS"],
                COLUNAS_CRIADAS["NOME_RESSELLER"],
            ]
        )

        grupos_de_sellers = contas_a_receber.groupby(COLUNAS_CRIADAS["SELLERS"])

        for seller, planilha_seller in grupos_de_sellers:
            print(f"Processando relatório para o seller: '{seller}.xlsx')")

            soma_dos_repasses = planilha_seller[COLUNAS_CRIADAS["TOTAL_REPASSE"]].sum()

            # cria um dataframe com a soma de repasses
            linha_total = pd.DataFrame(
                [
                    {
                        planilha_seller.columns[0]: "TOTAL",
                        COLUNAS_CRIADAS["TOTAL_REPASSE"]: soma_dos_repasses,
                    }
                ]
            )

            # junta o dataframe com a linha de total com o contas_a_receber
            planilha_com_total = pd.concat(
                [planilha_seller, linha_total], ignore_index=True
            )

            nome_arquivo = f"{seller}.xlsx"
            caminho_completo_do_arquivo = DIR_OUTPUT / nome_arquivo
            planilha_com_total.to_excel(caminho_completo_do_arquivo, index=False)

            print("Arquivos Salvos.")
    except Exception as e:
        raise FileNotFoundError(f"Erro ao salvar arquivos: {e}") from e
