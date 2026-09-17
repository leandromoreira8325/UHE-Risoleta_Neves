"""
processing.py
Download das bandas B04 e B08, cálculo do NDVI e mensuração da área em hectares.
"""

from __future__ import annotations

import os
from pathlib import Path
import requests
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np

from src.copernicus_api import CopernicusDataSpaceAPI


def baixar_banda(url: str, destino_path: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    with requests.get(url, headers=headers, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(destino_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def processar_cena_mensal(cena: dict) -> dict:
    data_cena = cena.get("data", "N/A")
    print(f"\n[PROCESSING] Baixando bandas B04 e B08 para {data_cena}...")

    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    os.makedirs(data_dir, exist_ok=True)

    b04_path = os.path.join(data_dir, f"B04_{data_cena}.jp2")
    b08_path = os.path.join(data_dir, f"B08_{data_cena}.jp2")

    api = CopernicusDataSpaceAPI()
    token = api.obter_token()

    if not os.path.exists(b04_path):
        baixar_banda(cena["B04"], b04_path, token)
    if not os.path.exists(b08_path):
        baixar_banda(cena["B08"], b08_path, token)

    # Carrega limite do reservatório para mascarar os rasters
    candidatos = list(base_dir.glob("*.shp")) + list(base_dir.glob("data/*.shp"))
    target_shp = max(candidatos, key=os.path.getmtime)
    gdf = gpd.read_file(target_shp)

    with rasterio.open(b04_path) as src_b04:
        # Reprojeta shapefile para o CRS nativo do Sentinel-2 (UTM)
        gdf_utm = gdf.to_crs(src_b04.crs)
        geometrias = [geom for geom in gdf_utm.geometry]

        out_b04, _ = mask(src_b04, geometrias, crop=True)
        banda_red = out_b04[0].astype(float)

    with rasterio.open(b08_path) as src_b08:
        out_b08, _ = mask(src_b08, geometrias, crop=True)
        banda_nir = out_b08[0].astype(float)

    # Cálculo do NDVI e isolamento de vegetação aquática (NDVI > 0.2)
    np.seterr(divide='ignore', invalid='ignore')
    ndvi = (banda_nir - banda_red) / (banda_nir + banda_red)
    
    pixels_macrophtas = np.sum((ndvi > 0.20) & (ndvi <= 1.0))

    # Resolução Sentinel-2: 10m x 10m = 100 m² = 0.01 ha por píxel
    area_macro_ha = float(pixels_macrophtas * 0.01)
    area_reservatorio_ha = 1450.0
    pct_ocupacao = (area_macro_ha / area_reservatorio_ha) * 100

    print(f"[PROCESSING] {data_cena} | Área de Macrófitas: {area_macro_ha:.2f} ha ({pct_ocupacao:.2f}%)")

    return {
        "mes_ref": data_cena[:7],
        "data_cena": data_cena,
        "nuvens": cena.get("nuvens", 0.0),
        "area_ha": area_macro_ha,
        "percentual": pct_ocupacao,
        "nome_produto": cena.get("nome_produto", ""),
    }
