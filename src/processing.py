"""
processing.py

Fluxo principal do monitoramento.
"""

from src.config import SHAPEFILE_PATH

from src.sentinel_search import (
    buscar_melhor_cena
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
        "[PROCESSING] Bandas disponíveis:"
    )

    print(
        f"B03: {cena['B03']}"
    )

    print(
        f"B04: {cena['B04']}"
    )

    print(
        f"B08: {cena['B08']}"
    )

    print(
        f"SCL: {cena['SCL']}"
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
