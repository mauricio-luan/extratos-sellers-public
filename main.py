"""Gera relatórios de contas a receber e comissões para cada seller"""

__author__ = "Mauricio Luan"
__status__ = "Production"


from extratos_sellers.load import load
from extratos_sellers.transform import transform
from extratos_sellers.save import save


def main() -> None:
    """Realiza as operações principais do processamento para todos sellers."""

    try:
        contas_a_receber, comissoes = load()
        contas_a_receber_final = transform(contas_a_receber, comissoes)
        save(contas_a_receber_final)

    except ValueError as e:
        print(f"Erro Load: {e}")

    except RuntimeError as e:
        print(f"Erro Transform: {e}")

    except FileNotFoundError as e:
        print(f"Erro Save: {e}")

    except Exception as e:
        print(f"Erro geral: {e}")


if __name__ == "__main__":
    main()
