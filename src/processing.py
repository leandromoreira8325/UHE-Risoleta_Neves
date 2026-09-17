"""
processing.py
Download das bandas B04, B08 e TCI (RGB), cálculo de NDVI, geração do mapa 
composto (Classificação + Cor Real) e limpeza automática de temporários.
"""

from __future__ import annotations

import os
from pathlib import Path
import requests
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

from src.copernicus_api import CopernicusDataSpaceAPI

AREA_RESERVATORIO_HA = 282.0


def baixar_banda_stream(url: str, destino_path: str, token: str) -> None:
    headers = {"Authorization": f"Bearer {token}"}
    with requests.get(url, headers=headers, stream=True, timeout=120) as response:
        response.raise_for_status()
        with open(destino_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


def processar_cena_mensal(cena: dict) -> dict:
    data_cena = cena.get("data", "N/A")
    print(f"\n[PROCESSING] Baixando bandas B04, B08 e TCI (RGB) para {data_cena}...")

    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    os.makedirs(data_dir, exist_ok=True)

    b04_path = data_dir / f"temp_B04_{data_cena}.jp2"
    b08_path = data_dir / f"temp_B08_{data_cena}.jp2"
    tci_path = data_dir / f"temp_TCI_{data_cena}.jp2"
    img_saida_path = data_dir / f"mapa_composto_{data_cena}.png"

    api = CopernicusDataSpaceAPI()
    token = api.obter_token()

    try:
        baixar_banda_stream(cena["B04"], str(b04_path), token)
        baixar_banda_stream(cena["B08"], str(b08_path), token)
        baixar_banda_stream(cena["TCI"], str(tci_path), token)

        candidatos = list(base_dir.glob("*.shp")) + list(base_dir.glob("data/*.shp"))
        if not candidatos:
            raise FileNotFoundError(f"[ERRO CRÍTICO] Nenhum .shp encontrado em '{base_dir}'.")

        target_shp = max(candidatos, key=os.path.getmtime)
        gdf = gpd.read_file(target_shp)

        # 1. Leitura e recorte de B04 e B08 (NDVI)
        with rasterio.open(b04_path) as src_b04:
            gdf_utm = gdf.to_crs(src_b04.crs)
            geometrias = [geom for geom in gdf_utm.geometry]
            out_b04, transform = mask(src_b04, geometrias, crop=True)
            banda_red = out_b04[0].astype(float)

        with rasterio.open(b08_path) as src_b08:
            out_b08, _ = mask(src_b08, geometrias, crop=True)
            banda_nir = out_b08[0].astype(float)

        # 2. Cálculo do NDVI e isolamento de macrófitas (NDVI > 0.20)
        np.seterr(divide="ignore", invalid="ignore")
        ndvi = (banda_nir - banda_red) / (banda_nir + banda_red)
        mask_macro = (ndvi > 0.20) & (ndvi <= 1.0)
        pixels_macro = np.sum(mask_macro)

        area_macro_ha = float(pixels_macro * 0.01)
        pct_ocupacao = (area_macro_ha / AREA_RESERVATORIO_HA) * 100

        print(f"[PROCESSING] {data_cena} | Área: {area_macro_ha:.2f} ha ({pct_ocupacao:.2f}%)")

        # 3. Leitura e recorte do TCI (Cor Real RGB)
        with rasterio.open(tci_path) as src_tci:
            out_tci, transform_tci = mask(src_tci, geometrias, crop=True)
            rgb = np.moveaxis(out_tci[:3], 0, -1)

        # 4. Construção da Figura Dupla no Matplotlib
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12), dpi=150)

        # Extensão espacial do raster recortado
        h, w = mask_macro.shape
        xmin = transform[2]
        xmax = xmin + transform[0] * w
        ymax = transform[5]
        ymin = ymax + transform[4] * h
        raster_extent = [xmin, xmax, ymin, ymax]

        # Painel Superior: Classificação Temática
        gdf_utm.plot(ax=ax1, facecolor="#87CEEB", edgecolor="#4682B4", linewidth=0.8, alpha=0.7)
        macro_display = np.where(mask_macro, 1.0, np.nan)
        cmap_macro = ListedColormap(["#D32F2F"])
        ax1.imshow(macro_display, extent=raster_extent, cmap=cmap_macro, alpha=0.9, zorder=3)

        patch_res = mpatches.Patch(color='#87CEEB', label=f'Reservatório ({AREA_RESERVATORIO_HA:.0f} ha)')
        patch_macro = mpatches.Patch(color='#D32F2F', label=f'Macrófitas ({area_macro_ha:.2f} ha - {pct_ocupacao:.2f}%)')
        ax1.legend(handles=[patch_res, patch_macro], loc='upper right', fontsize=8, framealpha=0.9)
        ax1.set_title(f"UHE Risoleta Neves - Classificação de Macrófitas ({data_cena})", fontsize=10, fontweight='bold')
        ax1.grid(True, linestyle="--", alpha=0.3)

        # Painel Inferior: Cor Real (TCI)
        h_tci, w_tci, _ = rgb.shape
        xmin_tci = transform_tci[2]
        xmax_tci = xmin_tci + transform_tci[0] * w_tci
        ymax_tci = transform_tci[5]
        ymin_tci = ymax_tci + transform_tci[4] * h_tci
        tci_extent = [xmin_tci, xmax_tci, ymin_tci, ymax_tci]

        ax2.imshow(rgb, extent=tci_extent)
        gdf_utm.plot(ax=ax2, facecolor='none', edgecolor='#FFD700', linewidth=1.0, linestyle='--')
        
        patch_tci_border = mpatches.Patch(facecolor='none', edgecolor='#FFD700', label='Limite do Reservatório')
        ax2.legend(handles=[patch_tci_border], loc='upper right', fontsize=8, framealpha=0.9)
        ax2.set_title(f"Imagem Sentinel-2 em Cor Real (RGB / TCI) - {data_cena}", fontsize=10, fontweight='bold')
        ax2.grid(True, linestyle="--", alpha=0.3)

        plt.tight_layout()
        plt.savefig(img_saida_path, bbox_inches="tight")
        plt.close(fig)

        return {
            "mes_ref": data_cena[:7],
            "data_cena": data_cena,
            "nuvens": cena.get("nuvens", 0.0),
            "area_ha": area_macro_ha,
            "percentual": pct_ocupacao,
            "nome_produto": cena.get("nome_produto", ""),
            "mapa_path": str(img_saida_path),
        }

    finally:
        for p in [b04_path, b08_path, tci_path]:
            if p.exists():
                try:
                    os.remove(p)
                except OSError:
                    pass
