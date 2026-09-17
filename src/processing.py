"""
processing.py
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
        "[PROCESSING] Próxima etapa: download das bandas B03, B04, B08 e SCL."
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
