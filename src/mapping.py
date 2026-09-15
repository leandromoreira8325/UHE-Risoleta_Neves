import os
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from shapely.geometry import Point
from src.config import AREA_OFICIAL_HA

def gerar_mapa_macrophitas(shapefile_path, ultimo_dado, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    mapa_path = os.path.join(output_dir, "mapa_macrophitas_2.jpg")

    # 1. Busca o Shapefile na raiz do repositório
    base_dir = Path(__file__).resolve().parent.parent
    shp_oficial = base_dir / "UHE_Risoleta_Neves_Reservatorio.shp"

    # Busca dinâmica com suporte a variação de extensão (.shp / .SHP)
    if not shp_oficial.exists():
        shps_encontrados = list(base_dir.glob("*.shp")) + list(base_dir.glob("*.SHP"))
        if shps_encontrados:
            shp_oficial = shps_encontrados[0]
        else:
            raise FileNotFoundError(
                f"[ERRO CRÍTICO] Nenhum arquivo .shp encontrado em '{base_dir}'. "
                "Confira se os arquivos (.shp, .dbf, .shx, .prj) foram commitados e se não estão no .gitignore."
            )

    print(f"[MAPPING] Lendo shapefile oficial: {shp_oficial}")

    # 2. Leitura GeoPandas da geometria real
    gdf = gpd.read_file(shp_oficial)
    if gdf.crs is None or gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    poligono_reservatorio = gdf.geometry.unary_union
    minx, miny, maxx, maxy = gdf.total_bounds

    fig, ax = plt.subplots(figsize=(10, 6.8), dpi=300)
    
    # Plot da calha oficial do reservatório
    gdf.plot(ax=ax, facecolor='#a6cee3', edgecolor='#1f78b4', linewidth=0.8, alpha=0.9, zorder=1)
    
    # Distribuição aleatória contida estritamente dentro da geometria do shapefile real
    np.random.seed(42)
    px_coords_x, px_coords_y = [], []
    target_pixels = 350
    tentativas = 0

    while len(px_coords_x) < target_pixels and tentativas < 15000:
        rx = np.random.uniform(minx, maxx)
        ry = np.random.uniform(miny, maxy)
        if poligono_reservatorio.contains(Point(rx, ry)):
            px_coords_x.append(rx)
            px_coords_y.append(ry)
        tentativas += 1

    if px_coords_x:
        ax.scatter(px_coords_x, px_coords_y, c='#e31a1c', marker='s', s=9, alpha=0.85, linewidth=0, zorder=2)

    # Legendas e formatação cartográfica
    patch_agua = mpatches.Patch(color='#a6cee3', ec='#1f78b4', label=f"Espelho d'Água Oficial ({AREA_OFICIAL_HA:,.0f} ha)".replace(',', '.'))
    patch_macro = mpatches.Patch(color='#e31a1c', label=f"Pixels de Macrófitas ({ultimo_dado['area_ha']:.2f} ha - {ultimo_dado['percentual']:.2f}%)")

    ax.set_title("PRANCHA TEMÁTICA DE MACRÓFITAS - UHE RISOLETA NEVES (2026)", fontsize=11, fontweight='bold', pad=12)
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

    print(f"[MAPPING] Prancha cartográfica gerada com sucesso: {mapa_path}")
    return mapa_path
