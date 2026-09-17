"""
processing.py
"""

from src.config import SHAPEFILE_PATH

from src.sentinel_search import (
    buscar_melhor_cena
)

from src.sentinel_download import (
    baixar_produto
)


def processar_dados_2026():

    print(
        "[PROCESSING] Iniciando processamento..."
    )

    cena = buscar_melhor_cena()

    if cena is None:

        raise RuntimeError(
            "Nenhuma cena Sentinel encontrada."
        )

    print(
        "[PROCESSING] Baixando cena..."
    )

    if (
        cena["product_id"] is not None
    ):

        baixar_produto(
            cena["product_id"],
            cena["nome_produto"]
        )

    dados_serie = [

        {
            "mes": str(
                cena["data"]
            )[:10],

            "area_ha": 0.0,

            "percentual": 0.0,

            "status": (
                f"Sentinel-2 "
                f"({cena['nuvens']}% nuvens)"
            )
        }
    ]

    return (
        dados_serie,
        str(SHAPEFILE_PATH)
    )
