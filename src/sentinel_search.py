"""
sentinel_search.py

Busca da melhor cena Sentinel-2 L2A
para o reservatório da UHE Risoleta Neves.
"""

from __future__ import annotations

import geopandas as gpd
import requests

from src.config import (
    SHAPEFILE_PATH,
    DATA_INICIAL,
    DATA_FINAL,
    NUVEM_MAXIMA
)

from src.copernicus_api import (
    CopernicusDataSpaceAPI
)


def obter_bbox():

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

    minx, miny, maxx, maxy = (
        gdf.total_bounds
    )

    return (
        minx,
        miny,
        maxx,
        maxy
    )


def buscar_melhor_cena():

    minx, miny, maxx, maxy = (
        obter_bbox()
    )

    print(
        "[SENTINEL] Consultando catálogo..."
    )

    api = CopernicusDataSpaceAPI()

    token = api.obter_token()

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    bbox = (
        f"{minx},{miny},{maxx},{maxy}"
    )

    url = (
        "https://catalogue.dataspace.copernicus.eu/"
        "resto/api/collections/"
        "SENTINEL-2/search.json"
    )

    params = {
        "box": bbox,
        "startDate": DATA_INICIAL,
        "completionDate": DATA_FINAL,
        "cloudCover":
        f"[0,{NUVEM_MAXIMA}]",
        "maxRecords": 25,
        "sortParam": "cloudCover",
        "sortOrder": "ascending"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=120
    )

    response.raise_for_status()

    resultado = response.json()

    features = resultado.get(
        "features",
        []
    )

    if len(features) == 0:

        raise RuntimeError(
            "Nenhuma cena Sentinel encontrada."
        )

    melhor = features[0]

    propriedades = melhor[
        "properties"
    ]

    cena = {
        "product_id":
            propriedades.get(
                "id"
            ),

        "nome_produto":
            propriedades.get(
                "title"
            ),

        "data":
            propriedades.get(
                "startDate"
            ),

        "nuvens":
            propriedades.get(
                "cloudCover",
                0
            )
    }

    print(
        "[SENTINEL] Melhor cena encontrada:"
    )

    print(
        cena["nome_produto"]
    )

    print(
        f"Nuvens: "
        f"{cena['nuvens']}%"
    )

    return cena


if __name__ == "__main__":

    cena = buscar_melhor_cena()

    print(cena)
