"""
mapping.py
Geração das pranchas cartográficas mensais com imagem real de NDVI e contorno do reservatório.
"""

from __future__ import annotations

import os
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import rasterio


def gerar_mapa_macrophitas(
    shapefile_path: str | None,
    ultimo_dado: dict,
    output_dir: str,
    sufixo: str = "",
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    nome_arquivo = f"mapa_macrophitas_{sufixo}.jpg" if sufixo else "mapa_macrophitas.jpg"
    mapa_path = os.path.join(output_dir, nome_arquivo)

    base_dir = Path(__file__).resolve().parent.parent

    # 1. Carrega o limite oficial do reservatório (Shapefile / GeoJSON)
    if shapefile_path and os.path.exists(shapefile_path):
        target_shp = shapefile_path
    else:
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
        gdf = gdf.to_crs("EPSG:4326")

    area_ha = ultimo_dado.get("area_ha", 0.0)
    pct = ultimo_dado.get("percentual", 0.0)
    data_str = ultimo_dado.get("data_cena", "")
    raster_path = ultimo_dado.get("raster_path") or ultimo_dado.get("ndvi_path")

    fig, ax = plt.subplots(figsize=(8, 10), dpi=300)

    # 2. Renderiza a Imagem Real do NDVI (se o raster GeoTIFF for fornecido)
    if raster_path and os.path.exists(raster_path):
        with rasterio.open(raster_path) as src:
            ndvi_arr = src.read(1)
            bounds = src.bounds
            extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

        # Filtra NoData e valores fora do intervalo válido [-1, 1]
        ndvi_masked = np.ma.masked_invalid(ndvi_arr)
        ndvi_masked = np.ma.masked_where((ndvi_masked < -1.0) | (ndvi_masked > 1.0), ndvi_masked)

        # Plot da resposta espectral contínua de fundo (YlGn)
        cmap_ndvi = plt.cm.get_cmap("YlGn")
        im = ax.imshow(
            ndvi_masked,
            extent=extent,
            cmap=cmap_ndvi,
            vmin=-0.1,
            vmax=0.7,
            origin="upper",
            alpha=0.75,
            zorder=1,
        )

        # Overlay destacando apenas os pixels de macrófitas (NDVI >= 0.35)
        limiar_ndvi = 0.35
        macro_mask = np.ma.masked_where(ndvi_arr < limiar_ndvi, ndvi_arr)
        cmap_macro = LinearSegmentedColormap.from_list("MacroRed", ["#ff7f00", "#e31a1c"])

        ax.imshow(
            macro_mask,
            extent=extent,
            cmap=cmap_macro,
            vmin=limiar_ndvi,
            vmax=0.8,
            origin="upper",
            alpha=0.9,
            zorder=2,
        )

        cbar = fig.colorbar(im, ax=ax, shrink=0.5, pad=0.03)
        cbar.set_label("NDVI Real (Sentinel-2)", fontsize=8)

    else:
        # Fallback vetorial simples caso o raster da cena não esteja acessível
        gdf.plot(
            ax=ax,
            facecolor="#a6cee3",
            edgecolor="#1f78b4",
            linewidth=0.6,
            alpha=0.85,
            zorder=1,
        )

    # 3. Desenha o perímetro do espelho d'água
    gdf.boundary.plot(
        ax=ax,
        color="#1f78b4",
        linewidth=0.8,
        linestyle="-",
        zorder=3,
    )

    # Legenda e Título com os 282 ha corrigidos
    patch_agua = mpatches.Patch(color="#1f78b4", fill=False, label="Espelho d'Água (282 ha)")
    patch_macro = mpatches.Patch(color="#e31a1c", label=f"Macrófitas ({area_ha:.2f} ha - {pct:.2f}%)")

    ax.set_title(
        f"UHE Risoleta Neves - Distribuição Real de Macrófitas ({data_str})\n"
        f"Acúmulo Mapeado: {area_ha:.2f} ha ({pct:.2f}% do espelho)",
        fontsize=10,
        fontweight="bold",
        pad=12,
    )
    ax.set_xlabel("Longitude (WGS84)", fontsize=8.5)
    ax.set_ylabel("Latitude (WGS84)", fontsize=8.5)
    ax.tick_params(labelsize=8)
    ax.grid(True, linestyle=":", alpha=0.4, zorder=0)
    ax.legend(handles=[patch_agua, patch_macro], loc="upper right", framealpha=0.95, fontsize=8.5)

    # Ajuste dos limites da visualização com margem
    minx, miny, maxx, maxy = gdf.total_bounds
    margin_x = (maxx - minx) * 0.04
    margin_y = (maxy - miny) * 0.04
    ax.set_xlim([minx - margin_x, maxx + margin_x])
    ax.set_ylim([miny - margin_y, maxy + margin_y])

    plt.tight_layout()
    plt.savefig(mapa_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"[MAPPING] Mapa NDVI real gerado: {mapa_path}")
    return mapa_path
