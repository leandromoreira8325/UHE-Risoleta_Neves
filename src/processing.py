"""
processing.py
Leitura remota por janela (vsicurl) das bandas B04 e B08, cálculo de NDVI e biomassa.
"""

from __future__ import annotations

import os
from pathlib import Path
import geopandas as gpd
import rasterio
from rasterio.windows import from_bounds
from rasterio.env import Env
import numpy as np

from src.copernicus_api import CopernicusDataSpaceAPI


def processar_cena_mensal(cena: dict) -> dict:
    data_cena = cena.get("data", "N/A")
    print(f"[PROCESSING] Lendo recorte do reservatório para {data_cena} via VSI...")

    base_dir = Path(__file__).resolve().parent.parent
    candidatos = list(base_dir.glob("*.shp")) + list(base_dir.glob("data/*.shp"))
    if not candidatos:
        raise FileNotFoundError(f"[ERRO] Nenhum .shp encontrado em '{base_dir}'.")
        
    target_shp = max(candidatos, key=os.path.getmtime)
    gdf = gpd.read_file(target_shp)

    api = CopernicusDataSpaceAPI()
    token = api.obter_token()

    header_auth = f"Authorization: Bearer {token}"

    # Utiliza /vsicurl/ para baixar apenas o trecho do reservatório sem baixar o arquivo JP2 inteiro
    with Env(GDAL_HTTP_HEADER_INSERT=header_auth, CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".jp2"):
        # Banda Vermelha (B04)
        with rasterio.open(f"/vsicurl/{cena['B04']}") as src_b04:
            gdf_utm = gdf.to_crs(src_b04.crs)
            minx, miny, maxx, maxy = gdf_utm.total_bounds
            window = from_bounds(minx, miny, maxx, maxy, src_b04.transform)
            banda_red = src_b04.read(1, window=window).astype(float)

        # Banda Infravermelho Próximo (B08)
        with rasterio.open(f"/vsicurl/{cena['B08']}") as src_b08:
            banda_nir = src_b08.read(1, window=window).astype(float)

    # Cálculo do NDVI na janela
    np.seterr(divide="ignore", invalid="ignore")
    ndvi = (banda_nir - banda_red) / (banda_nir + banda_red)

    # Identificação de pixels de macrófitas (NDVI > 0.2)
    pixels_macro = np.sum((ndvi > 0.20) & (ndvi <= 1.0))

    # Resolução Sentinel-2: 10m x 10m = 100 m² = 0.01 ha por pixel
    area_macro_ha = float(pixels_macro * 0.01)
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
