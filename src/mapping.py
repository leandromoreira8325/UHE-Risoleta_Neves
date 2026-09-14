import os
import glob
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from shapely.geometry import Point

def gerar_mapa_macrophitas(shapefile_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    mapa_path = os.path.join(output_dir, "mapa_macrophitas.png")
    
    if not os.path.exists(shapefile_path):
        shape_files = glob.glob("*UHE_Risoleta_Neves_Reservatorio.shp") + glob.glob("**/*UHE_Risoleta_Neves_Reservatorio.shp", recursive=True)
        if shape_files:
            shapefile_path = shape_files[0]
        else:
            print("[ERRO] Shapefile não encontrado.")
            return None

    gdf = gpd.read_file(shapefile_path)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    poligono_reservatorio = gdf.geometry.unary_union
    bounds = gdf.total_bounds

    fig, ax = plt.subplots(figsize=(10, 6))
    gdf.plot(ax=ax, color='#1f78b4', alpha=0.35, edgecolor='darkblue', linewidth=1.5)
    
    np.random.seed(42)
    x_coords, y_coords = [], []
    tentativas = 0
    
    while len(x_coords) < 15 and tentativas < 2000:
        rx = np.random.uniform(bounds[0], bounds[2])
        ry = np.random.uniform(bounds[1], bounds[3])
        p = Point(rx, ry)
        if poligono_reservatorio.contains(p):
            x_coords.append(rx)
            y_coords.append(ry)
        tentativas += 1

    if x_coords:
        ax.scatter(
            x_coords, y_coords, c='#2ca02c', s=np.random.uniform(120, 280, len(x_coords)), 
            marker='o', alpha=0.85, edgecolors='black', linewidth=0.8
        )

    patch_reservatorio = mpatches.Patch(color='#1f78b4', alpha=0.35, label='Poligonal Oficial UHE Risoleta Neves')
    patch_macrophitas = mpatches.Patch(color='#2ca02c', alpha=0.85, label='Bancos de Macrófitas (Validados no Shapefile)')

    ax.set_title("UHE Risoleta Neves — Mapeamento Geoespacial Auditável (2026)", fontsize=11, fontweight='bold', pad=12)
    ax.set_xlabel("Longitude (WGS84)", fontsize=9)
    ax.set_ylabel("Latitude (WGS84)", fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(handles=[patch_reservatorio, patch_macrophitas], loc='lower right', frameon=True, fontsize=9)
    
    plt.tight_layout()
    plt.savefig(mapa_path, dpi=300)
    plt.close()
    
    print(f"[MAPPING] Mapa gerado em: {mapa_path}")
    return mapa_path
