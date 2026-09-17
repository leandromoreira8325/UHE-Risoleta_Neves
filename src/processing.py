"""
processing.py
Download streaming rápido das bandas B04 e B08, cálculo do NDVI e limpeza automática.
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


def baixar_banda_stream(url: str, destino_path: str, token: str) -> None:
    headers = {"Authorization": f"Bearer {token}"}
    with requests.get(url, headers=headers, stream=True, timeout=120) as response:
        response.raise_for_status()
        with open(destino_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):  # Chunks de 1MB
                if chunk:
                    f.write(chunk)


def processar_cena_mensal(cena: dict) -> dict:
    data_cena = cena.get("data", "N/A")
    print(f"[PROCESSING] Baixando bandas B04 e B08 para {data_cena}...")

    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    os.makedirs(data_dir, exist_ok=True)

    b04_path = data_dir / f"temp_B04_{data_cena}.jp2"
    b08_path = data_dir / f"temp_B08_{data_cena}.jp2"

    api = CopernicusDataSpaceAPI()
    token = api.obter_token()

    try:
        baixar_banda_stream(cena["B04"], str(b04_path), token)
        baixar_banda_stream(cena["B08"], str(b08_path), token)

        candidatos = list(base_dir.glob("*.shp")) + list(base_dir.glob("data/*.shp"))
        if not candidatos:
            raise FileNotFoundError(f"[ERRO CRÍTICO] Nenhum .shp encontrado em '{base_dir}'.")

        target_shp = max(candidatos, key=os.path.getmtime)
        gdf = gpd.read_file(target_shp)

        with rasterio.open(b04_path) as src_b04:
            gdf_utm = gdf.to_crs(src_b04.crs)
            geometrias = [geom for geom in gdf_utm.geometry]
            out_b04, _ = mask(src_b04, geometrias, crop=True)
            banda_red = out_b04[0].astype(float)

        with rasterio.open(b08_path) as src_b08:
            out_b08, _ = mask(src_b08, geometrias, crop=True)
            banda_nir = out_b08[0].astype(float)

        np.seterr(divide="ignore", invalid="ignore")
        ndvi = (banda_nir - banda_red) / (banda_nir + banda_red)

        pixels_macro = np.sum((ndvi > 0.20) & (ndvi <= 1.0))

        # Resolução Sentinel-2: 10m x 10m = 100 m² = 0.01 ha por pixel
        area_macro_ha = float(pixels_macro * 0.01)
        area_reservatorio_ha = 282.0  # Área corrigida do reservatório
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

    finally:
        if b04_path.exists():
            os.remove(b04_path)
        if b08_path.exists():
            os.remove(b08_path)
