"""
sentinel_search.py

Consulta Sentinel-2 via STAC.
"""

from __future__ import annotations

import geopandas as gpd

from pystac_client import Client

from src.config import SHAPEFILE_PATH


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

    print(
        "[SENTINEL] Catálogo acessado."
    )

    print(
        "\nCOLEÇÕES DISPONÍVEIS:\n"
    )

    for collection in (
        catalog.get_collections()
    ):

        print(collection.id)

    return {
        "product_id": None,
        "nome_produto": None,
        "data": "2026-09-15",
        "nuvens": 0.0
    }


if __name__ == "__main__":

    buscar_melhor_cena()
``
