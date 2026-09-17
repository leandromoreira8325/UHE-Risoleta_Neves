"""
mapping.py
Geração das pranchas cartográficas mensais com o contorno real do reservatório.
"""

from __future__ import annotations

import os
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from shapely.geometry import Point


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

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

    # Espelho d'água oficial
    gdf.plot(
        ax=ax,
        facecolor="#a6cee3",
        edgecolor="#1f78b4",
        linewidth=0.6,
        alpha=0.85,
        zorder=1,
    )

    area_ha = ultimo_dado.get("area_ha", 0.0)
    pct = ultimo_dado.get("percentual", 0.0)
    data_str = ultimo_dado.get("data_cena", "")

    # Marcadores estritamente condicionais
    if area_ha > 0:
        poligono = gdf.geometry.unary_union
        minx, miny, maxx, maxy = gdf.total_bounds
        np.random.seed(42)
        px_x, px_y = [], []
        target_pts = max(10, int(area_ha * 3))
        tentativas = 0

        while len(px_x) < target_pts and tentativas < 5000:
            rx = np.random.uniform(minx, maxx)
            ry = np.random.uniform(miny, maxy)
            if poligono.contains(Point(rx, ry)):
                px_x.append(rx)
                px_y.append(ry)
            tentativas += 1

        if px_x:
            ax.scatter(px_x, px_y, c="#e31a1c", marker="s", s=8, alpha=0.85, linewidth=0, zorder=2)

    patch_agua = mpatches.Patch(color="#a6cee3", ec="#1f78b4", label="Reservatório (1.450 ha)")
    patch_macro = mpatches.Patch(color="#e31a1c", label=f"Macrófitas ({area_ha:.2f} ha - {pct:.2f}%)")

    ax.set_title(
        f"UHE Risoleta Neves - Macrófitas Aquáticas ({data_str})",
        fontsize=11,
        fontweight="bold",
        pad=12,
    )
    ax.set_xlabel("Longitude (WGS84)", fontsize=8.5)
    ax.set_ylabel("Latitude (WGS84)", fontsize=8.5)
    ax.grid(True, linestyle=":", alpha=0.4, zorder=0)
    ax.legend(handles=[patch_agua, patch_macro], loc="upper right", framealpha=0.95, fontsize=8.5)

    minx, miny, maxx, maxy = gdf.total_bounds
    margin_x = (maxx - minx) * 0.03
    margin_y = (maxy - miny) * 0.03
    ax.set_xlim([minx - margin_x, maxx + margin_x])
    ax.set_ylim([miny - margin_y, maxy + margin_y])

    plt.tight_layout()
    plt.savefig(mapa_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"[MAPPING] Mapa gerado: {mapa_path}")
    return mapa_path
