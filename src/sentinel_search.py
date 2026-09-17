"""
sentinel_search.py

Busca da melhor cena Sentinel-2 L2A
e exibe todo o conteúdo STAC para
identificar o link correto de download.
"""

from __future__ import annotations

import json

import geopandas as gpd

from pystac_client import Client

from src.config import (
    SHAPEFILE_PATH,
    DATA_INICIAL,
    DATA_FINAL,
    NUVEM_MAXIMA
)

STAC_URL = (
    "https://catalogue.dataspace.copernicus.eu/stac"
)


def obter_geometria():

    gdf = gpd.read_file(
        SHAPEFILE_PATH
    )

    if gdf.crs.to_epsg() != 4326:

        gdf = gdf.to_crs(
            epsg=4326
        )

    return (
        gdf.unary_union
        .__geo_interface__
    )


def buscar_melhor_cena():

    catalog = Client.open(
        STAC_URL
    )

    geometria = obter_geometria()

    search = catalog.search(
        collections=[
            "sentinel-2-l2a"
        ],
        intersects=geometria,
        datetime=(
            f"{DATA_INICIAL}/"
            f"{DATA_FINAL}"
        ),
        query={
            "eo:cloud_cover": {
                "lt": NUVEM_MAXIMA
            }
        }
    )

    itens = list(
        search.items()
    )

    if not itens:

        raise RuntimeError(
            "Nenhuma cena encontrada."
        )

    itens.sort(
        key=lambda item:
        item.properties.get(
            "eo:cloud_cover",
            100
        )
    )

    melhor = itens[0]

    print(
        "\nITEM STAC COMPLETO\n"
    )

    print(
        json.dumps(
            melhor.to_dict(),
            indent=2,
            ensure_ascii=False
        )
    )

    return {
        "uuid": melhor.id,
        "product_id": melhor.id,
        "nome_produto": melhor.id,
        "data": str(
            melhor.datetime
        ),
        "nuvens": melhor.properties.get(
            "eo:cloud_cover",
            0
        )
    }


if __name__ == "__main__":

    buscar_melhor_cena()
