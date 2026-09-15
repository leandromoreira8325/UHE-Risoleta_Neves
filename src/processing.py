"""
processing.py

Orquestra o fluxo principal de processamento.

Versão preparada para futura integração
com Sentinel-2 e Copernicus Data Space.
"""

from pathlib import Path

from src.config import SHAPEFILE_PATH
from src.sentinel_search import obter_bbox


def processar_dados_2026():
    """
    Fluxo principal de processamento.

    Retorna:
        dados_serie
        shapefile_path
    """

    print(
        "[PROCESSING] Iniciando processamento..."
    )

    if not SHAPEFILE_PATH.exists():

        raise FileNotFoundError(
            f"Shapefile não encontrado: "
            f"{SHAPEFILE_PATH}"
        )

    bbox = obter_bbox()

    print(
        f"[PROCESSING] BBOX encontrado: "
        f"{bbox}"
    )

    # ==================================================
    # TEMPORÁRIO
    # Até a implementação do download Sentinel-2
    # ==================================================

    dados_serie = [
        {
            "mes": "Set/2026",
            "area_ha": 123.25,
            "percentual": 8.50,
            "status": "Processamento Preparado para Sentinel-2"
        }
    ]

    print(
        "[PROCESSING] Processamento concluído."
    )

    return (
        dados_serie,
        str(SHAPEFILE_PATH)
    )
