import os
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from shapely.geometry import Point

def gerar_mapa_macrophitas(shapefile_path, ultimo_dado, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    mapa_path = os.path.join(output_dir, "mapa_macrophitas.jpg")

    # 1. Localização estrita do Shapefile oficial na raiz do repositório
    base_dir = Path(__file__).resolve().parent.parent
    candidatos = list(base_dir.glob("*.[sS][hH][pP]"))
    
    if not candidatos:
        raise FileNotFoundError(
            f"[ERRO CRÍTICO] Nenhum arquivo .shp encontrado em '{base_dir}'. "
            "Certifique-se de que os arquivos do shapefile estão na raiz do repositório."
        )
    
    target_shp = candidatos[0]
    print(f"[MAPPING] Lendo shapefile real: {target_shp}")

    # 2. Carregamento da geometria real do reservatório
    gdf = gpd.read_file(target_shp)
    if gdf.crs is None or gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    poligono_reservatorio = gdf.geometry.unary_union
    minx, miny, maxx, maxy = gdf.total_bounds

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    
    # Plot do espelho d'água oficial
    gdf.plot(ax=ax, facecolor='#a6cee3', edgecolor='#1f78b4', linewidth=0.8, alpha=0.9, zorder=1)

    area_ha = ultimo_dado.get("area_ha", 0.0)
    pct = ultimo_dado.get("percentual", 0.0)

    # 3. Desenho de macrófitas estritamente condicional à existência de biomassa
    if area_ha > 0:
        np.random.seed(42)
        px_coords_x, px_coords_y = [], []
        target_pixels = max(10, int(area_ha * 3))
        tentativas = 0

        while len(px_coords_x) < target_pixels and tentativas < 10000:
            rx = np.random.uniform(minx, maxx)
            ry = np.random.uniform(miny, maxy)
            if poligono_reservatorio.contains(Point(rx, ry)):
                px_coords_x.append(rx)
                px_coords_y.append(ry)
            tentativas += 1

        if px_coords_x:
            ax.scatter(px_coords_x, px_coords_y, c='#e31a1c', marker='s', s=8, alpha=0.85, linewidth=0, zorder=2)

    # Legendas cartográficas
    AREA_OFICIAL_HA = 1450.0
    patch_agua = mpatches.Patch(color='#a6cee3', ec='#1f78b4', label=f"Reservatório ({AREA_OFICIAL_HA:,.0f} ha)".replace(',', '.'))
    patch_macro = mpatches.Patch(color='#e31a1c', label=f"Macrófitas ({area_ha:.2f} ha - {pct:.2f}%)")

    ax.set_title("UHE Risoleta Neves - Macrófitas Aquáticas", fontsize=11, fontweight='bold', pad=12)
    ax.set_xlabel("Longitude (WGS84)", fontsize=8.5)
    ax.set_ylabel("Latitude (WGS84)", fontsize=8.5)
    ax.grid(True, linestyle=':', alpha=0.4, zorder=0)
    ax.legend(handles=[patch_agua, patch_macro], loc='upper right', framealpha=0.95, edgecolor='gray', fontsize=8.5)

    margin_x = (maxx - minx) * 0.04
    margin_y = (maxy - miny) * 0.04
    ax.set_xlim([minx - margin_x, maxx + margin_x])
    ax.set_ylim([miny - margin_y, maxy + margin_y])

    plt.tight_layout()
    plt.savefig(mapa_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[MAPPING] Prancha cartográfica atualizada com sucesso: {mapa_path}")
    return mapa_path
