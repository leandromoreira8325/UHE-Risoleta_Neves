"""
sentinel_search.py

Consulta ao catálogo STAC do
Copernicus Data Space.
"""

from __future__ import annotations

import geopandas as gpd

from pystac_client import Client

from src.config import (
    SHAPEFILE_PATH,
    DATA_INICIAL,
    DATA_FINAL
)


STAC_URL = (
    "https://catalogue.dataspace.copernicus.eu/stac"
)


def obter_geometria():

    gdf = gpd.read_file(
        SHAPEFILE_PATH
    )

    if gdf.crs is None:

        raise ValueError(
            "Shapefile sem CRS."
        )

    if gdf.crs.to_epsg() != 4326:

        gdf = gdf.to_crs(
            epsg=4326
        )

    return (
        gdf.unary_union
        .__geo_interface__
    )


def listar_colecoes():

    catalog = Client.open(
        STAC_URL
    )

    print(
        "\nCOLEÇÕES DISPONÍVEIS:\n"
    )

    for collection in (
        catalog.get_collections()
    ):

        print(
            collection.id
        )


def buscar_melhor_cena():

    geometria = obter_geometria()

    print(
        "[SENTINEL] Geometria carregada."
    )

    return {
        "id": "TEMPORARIO",
        "data": "2026-09-15",
        "nuvens": 0.0
    }


if __name__ == "__main__":

    listar_colecoes()
