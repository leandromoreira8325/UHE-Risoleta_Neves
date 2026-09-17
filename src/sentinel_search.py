"""
sentinel_search.py

Busca da melhor cena Sentinel-2 L2A via Bounding Box (bbox).
"""

from __future__ import annotations

import os
from pathlib import Path
import geopandas as gpd
from pystac_client import Client

from src.config import (
    DATA_INICIAL,
    DATA_FINAL,
    NUVEM_MAXIMA
)

STAC_URL = "https://catalogue.dataspace.copernicus.eu/stac"


def obter_bbox():
    base_dir = Path(__file__).resolve().parent.parent
    candidatos = list(base_dir.glob("*.shp")) + list(base_dir.glob("data/*.shp")) + list(base_dir.glob("*.[sS][hH][pP]"))

    if not candidatos:
        raise FileNotFoundError(
            f"[ERRO CRÍTICO] Nenhum arquivo .shp encontrado em '{base_dir}'. "
            "Certifique-se de que os arquivos do Shapefile foram enviados ao repositório."
        )

    target_shp = max(candidatos, key=os.path.getmtime)
    print(f"[SENTINEL_SEARCH] Lendo limite vetorial: {target_shp.name}")

    gdf = gpd.read_file(target_shp)

    if gdf.crs is None or str(gdf.crs).lower() != "epsg:4326":
        gdf = gdf.to_crs(epsg=4326)

    # Retorna [minx, miny, maxx, maxy] para garantir compatibilidade com a API STAC
    return list(gdf.total_bounds)


def buscar_melhor_cena():
    catalog = Client.open(STAC_URL)

    bbox = obter_bbox()

    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{DATA_INICIAL}/{DATA_FINAL}",
        query={
            "eo:cloud_cover": {
                "lt": NUVEM_MAXIMA
            }
        }
    )

    itens = list(search.items())

    if not itens:
        raise RuntimeError(
            "[ERRO] Nenhuma cena Sentinel-2 encontrada no catálogo para a extensão e datas informadas."
        )

    itens.sort(
        key=lambda item: item.properties.get("eo:cloud_cover", 100)
    )

    melhor = itens[0]

    privado = melhor.properties.get("_private", {})
    assets = melhor.to_dict()["assets"]

    cena = {
        "uuid": privado.get("product_uuid"),
        "nome_produto": privado.get("product_name"),
        "data": str(melhor.datetime),
        "nuvens": melhor.properties.get("eo:cloud_cover", 0),
        "B03": assets["B03_10m"]["alternate"]["https"]["href"],
        "B04": assets["B04_10m"]["alternate"]["https"]["href"],
        "B08": assets["B08_10m"]["alternate"]["https"]["href"],
        "SCL": assets["SCL_20m"]["alternate"]["https"]["href"]
    }

    print("\n[SENTINEL] Melhor cena encontrada:")
    print(cena["nome_produto"])
    print(f"Nuvens: {cena['nuvens']}%")

    return cena
