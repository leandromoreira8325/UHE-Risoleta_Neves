"""
sentinel_search.py

Consulta cenas Sentinel-2 no Copernicus Data Space Ecosystem.

Projeto:
Monitoramento de Macrófitas Aquáticas
UHE Risoleta Neves
"""

from __future__ import annotations

import requests
import geopandas as gpd

from typing import Optional

from src.config import (
    SHAPEFILE_PATH,
    DATA_INICIAL,
    DATA_FINAL,
    NUVEM_MAXIMA,
)

from src.copernicus_api import CopernicusDataSpaceAPI


CATALOG_URL = (
    "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
)


def obter_bbox() -> str:
    """
    Extrai o bounding box do shapefile.

    Returns
    -------
    str
        xmin,ymin,xmax,ymax
    """

    gdf = gpd.read_file(SHAPEFILE_PATH)

    if gdf.crs is None:
        raise ValueError(
            "Shapefile sem CRS definido."
        )

    if gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    minx, miny, maxx, maxy = gdf.total_bounds

    return f"{minx},{miny},{maxx},{maxy}"


def buscar_melhor_cena() -> Optional[dict]:
    """
    Busca a melhor cena Sentinel-2.

    Critérios:
    - menor cobertura de nuvens
    - dentro do período configurado

    Returns
    -------
    dict | None
    """

    bbox = obter_bbox()

   nicusDataSpaceAPI()

    token = api.obter_token()

    headers = {}

    if token:
        headers["Authorization"] = (
            f"Bearer {token}"
        )

    filtro = (
        f"Collection/Name eq 'SENTINEL-2' "
    )

    try:

        print(
            "[SENTINEL] Consultando catálogo..."
        )

        response = requests.get(
            CATALOG_URL,
            headers=headers,
            params={
                "$top": 100
            },
            timeout=60
        )

        response.raise_for_status()

        registros = response.json().get(
            "value",
            []
        )

        if not registros:

            print(
                "[SENTINEL] Nenhuma cena encontrada."
            )

            return None

        melhor = registros[0]

        resultado = {
            "id": melhor.get("Id"),
            "nome": melhor.get("Name"),
            "data": melhor.get("ContentDate", {}),
            "bbox": bbox,
        }

        print(
            "[SENTINEL] Cena encontrada:"
        )

        print(resultado)

        return resultado

    except requests.exceptions.RequestException as exc:

        print(
            f"[SENTINEL ERRO] {exc}"
        )

        return None


if __name__ == "__main__":

    cena = buscar_melhor_cena()

    print(cena)
