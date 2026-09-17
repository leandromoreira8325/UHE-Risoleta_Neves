"""
sentinel_search.py
Busca da melhor cena Sentinel-2 L2A com suporte a TCI (RGB) e sessão customizada para evitar bloqueio WAF.
"""

from __future__ import annotations

import os
from pathlib import Path
import geopandas as gpd
import requests
from pystac.stac_io import DefaultStacIO
from pystac_client import Client

STAC_URL = "https://catalogue.dataspace.copernicus.eu/stac"


class CustomStacIO(DefaultStacIO):
    """
    Classe IO customizada para injetar o User-Agent em TODAS as chamadas HTTP
    feitas pelo pystac_client, garantindo que requisições filhas/paginadas não sejam 
    bloqueadas pelo WAF/Cloudflare no GitHub Actions.
    """
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })


def obter_bbox() -> list[float]:
    base_dir = Path(__file__).resolve().parent.parent
    candidatos = (
        list(base_dir.glob("*.shp"))
        + list(base_dir.glob("data/*.shp"))
        + list(base_dir.glob("*.[sS][hH][pP]"))
    )

    if not candidatos:
        raise FileNotFoundError(f"[ERRO CRÍTICO] Nenhum arquivo .shp encontrado em '{base_dir}'.")

    target_shp = max(candidatos, key=os.path.getmtime)
    gdf = gpd.read_file(target_shp)

    if gdf.crs is None or str(gdf.crs).lower() != "epsg:4326":
        gdf = gdf.to_crs(epsg=4326)

    return list(gdf.total_bounds)


def buscar_melhor_cena(data_inicial: str, data_final: str) -> dict | None:
    # Utiliza a classe StacIO customizada com User-Agent persistente em todas as requisições
    catalog = Client.open(STAC_URL, stac_io=CustomStacIO())
    bbox = obter_bbox()

    for limite_nuvens in [20, 50]:
        search = catalog.search(
            collections=["sentinel-2-l2a"],
            bbox=bbox,
            datetime=f"{data_inicial}/{data_final}",
            query={"eo:cloud_cover": {"lt": limite_nuvens}},
        )

        itens = list(search.items())
        if itens:
            break

    if not itens:
        print(f"[AVISO] Nenhuma cena disponível entre {data_inicial} e {data_final}.")
        return None

    itens.sort(key=lambda item: item.properties.get("eo:cloud_cover", 100))
    melhor = itens[0]

    privado = melhor.properties.get("_private", {})
    assets = melhor.to_dict()["assets"]

    cena = {
        "uuid": privado.get("product_uuid"),
        "nome_produto": privado.get("product_name"),
        "data": str(melhor.datetime)[:10],
        "nuvens": melhor.properties.get("eo:cloud_cover", 0),
        "B03": assets["B03_10m"]["alternate"]["https"]["href"],
        "B04": assets["B04_10m"]["alternate"]["https"]["href"],
        "B08": assets["B08_10m"]["alternate"]["https"]["href"],
        "TCI": assets["TCI_10m"]["alternate"]["https"]["href"],
        "SCL": assets["SCL_20m"]["alternate"]["https"]["href"],
    }

    print(f"[SENTINEL] {cena['data']} | Produto: {cena['nome_produto']} | Nuvens: {cena['nuvens']}%")
    return cena
