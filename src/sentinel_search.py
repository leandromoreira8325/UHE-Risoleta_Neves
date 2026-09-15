"""
sentinel_search.py

Busca de cenas Sentinel-2 utilizando
o catálogo STAC do Copernicus Data Space.

Projeto:
Monitoramento de Macrófitas
UHE Risoleta Neves
"""

from __future__ import annotations

import geopandas as gpd
from pystac_client import Client

from src.config import (
    SHAPEFILE_PATH,
    DATA_INICIAL,
    DATA_FINAL,
    NUVEM_MAXIMA
)

CATALOGO_STAC = (
    "https://catalogue.dataspace.copernicus.eu/stac"
)


def obter_geometria_geojson():

    gdf = gpd.read_file(SHAPEFILE_PATH)

    if gdf.crs is None:

        raise ValueError(
            "Shapefile sem CRS definido."
        )

    if gdf.crs.to_epsg() != 4326:

        gdf = gdf.to_crs(
            epsg=4326
        )

    return gdf.unary_union.__geo_interface__


def buscar_melhor_cena():

    print(
        "[SENTINEL] Conectando ao catálogo STAC..."
    )

    catalog = Client.open(
        CATALOGO_STAC
    )

    geometria = obter_geometria_geojson()

    print(
        "[SENTINEL] Buscando cenas..."
    )

    search = catalog.search(

        collections=[
            "SENTINEL-2"
        ],

        intersects=geometria,

        datetime=f"{DATA_INICIAL}/{DATA_FINAL}",

        query={
            "eo:cloud_cover": {
                "lt": NUVEM_MAXIMA
            }
        }
    )

    itens = list(
        search.items()
    )

    if len(itens) == 0:

        print(
            "[SENTINEL] Nenhuma cena encontrada."
        )

        return None

    itens.sort(
        key=lambda x:
        x.properties.get(
            "eo:cloud_cover",
            999
        )
    )

    melhor = itens[0]

    resultado = {

        "id":
            melhor.id,

        "data":
            melhor.datetime,

        "nuvens":
            melhor.properties.get(
                "eo:cloud_cover"
            ),

        "assets":
            list(
                melhor.assets.keys()
            ),

        "item":
            melhor
    }

    print(
        "\n[SENTINEL] Melhor cena encontrada:"
    )

    print(
        f"ID: {resultado['id']}"
    )

    print(
        f"Data: {resultado['data']}"
    )

    print(
        f"Nuvens: {resultado['nuvens']} %"
    )

    return resultado


if __name__ == "__main__":

    cena = buscar_melhor_cena()

    print(cena)
