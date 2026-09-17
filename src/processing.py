"""
processing.py
"""

from src.config import SHAPEFILE_PATH

from src.sentinel_search import (
    buscar_melhor_cena
)

from src.sentinel_band_download import (
    baixar_bandas_principais
)


def processar_dados_2026():

    print(
        "[PROCESSING] Iniciando processamento..."
    )

    cena = buscar_melhor_cena()

    print(
        "[PROCESSING] Cena Sentinel localizada."
    )

    print(
        "[PROCESSING] Testando download da B03..."
    )

    baixar_bandas_principais(
        cena
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
        str(
            SHAPEFILE_PATH
        )
    )
