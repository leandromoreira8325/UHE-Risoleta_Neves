"""
sentinel_search.py

Busca de cenas Sentinel-2.
"""

from __future__ import annotations

import geopandas as gpd

from src.config import SHAPEFILE_PATH


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

    return {
        "xmin": float(minx),
        "ymin": float(miny),
        "xmax": float(maxx),
        "ymax": float(maxy)
    }


def buscar_melhor_cena():

    bbox = obter_bbox()

    print(
        f"[SENTINEL] BBOX: {bbox}"
    )

    #
    # TEMPORÁRIO
    # Enquanto implementamos a consulta
    # real ao catálogo STAC
    #

    return {
        "product_id": None,
        "nome_produto": None,
        "data": "2026-09-15",
        "nuvens": 0.0,
        "bbox": bbox
    }


if __name__ == "__main__":

    print(
        buscar_melhor_cena()
    )
