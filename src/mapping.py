import os
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import rasterio
from rasterio.mask import mask
import numpy as np
from src.config import AREA_OFICIAL_HA, SHAPEFILE_PATH

def gerar_mapa_macrophitas(shapefile_path, ultimo_dado, output_dir, raster_path=None):
    os.makedirs(output_dir, exist_ok=True)
    mapa_path = os.path.join(output_dir, "mapa_macrophitas_2.jpg")

    # 1. Carregamento Obrigatório do Shapefile Oficial
    target_shp = shapefile_path if os.path.exists(shapefile_path) else SHAPEFILE_PATH
    
    if not os.path.exists(target_shp):
        raise FileNotFoundError(f"[ERRO CRÍTICO] Shapefile não localizado em: {target_shp}")

    gdf = gpd.read_file(target_shp)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    
    # Renderização da calha d'água oficial da UHE Risoleta Neves
    gdf.plot(ax=ax, facecolor='#a6cee3', edgecolor='#1f78b4', linewidth=0.8, alpha=0.95, zorder=1)

    # 2. Processamento de Pixels Reais da Imagem Copernicus/Sentinel-2 (se disponível)
    if raster_path and os.path.exists(raster_path):
        with rasterio.open(raster_path) as src:
            # Recorta a imagem Copernicus estritamente pelo polígono do reservatório
            shapes = [geom for geom in gdf.geometry]
            out_image, out_transform = mask(src, shapes, crop=True)
            ndvi_matrix = out_image[0]
            
            # Limiar de NDVI para biomassa (ex: NDVI > 0.35)
            y_indices, x_indices = np.where(ndvi_matrix > 0.35)
            
            # Converte coordenadas de matriz em WGS84
            lon_coords, lat_coords = rasterio.transform.xy(out_transform, y_indices, x_indices)
            
            ax.scatter(
                lon_coords, lat_coords, 
                c='#e31a1c', marker='s', s=8, alpha=0.85, linewidth=0, zorder=2,
                label="Pixels de Macrófitas (NDVI > Limiar)"
            )
    
    # Ajustes Cartográficos
    minx, miny, maxx, maxy = gdf.total_bounds
    margin_x = (maxx - minx) * 0.05
    margin_y = (maxy - miny) * 0.05
    ax.set_xlim([minx - margin_x, maxx + margin_x])
    ax.set_ylim([miny - margin_y, maxy + margin_y])

    patch_agua = mpatches.Patch(color='#a6cee3', ec='#1f78b4', label=f"Espelho d'Água Oficial ({AREA_OFICIAL_HA:,.0f} ha)".replace(',', '.'))
    patch_macro = mpatches.Patch(color='#e31a1c', label=f"Pixels de Macrófitas ({ultimo_dado['area_ha']:.2f} ha - {ultimo_dado['percentual']:.2f}%)")

    ax.set_title("PRANCHA TEMÁTICA DE MACRÓFITAS - UHE RISOLETA NEVES (2026)", fontsize=11, fontweight='bold', pad=12)
    ax.set_xlabel("Longitude (WGS84)", fontsize=8.5)
    ax.set_ylabel("Latitude (WGS84)", fontsize=8.5)
    ax.grid(True, linestyle=':', alpha=0.4, zorder=0)
    ax.legend(handles=[patch_agua, patch_macro], loc='upper right', framealpha=0.95, edgecolor='gray', fontsize=8.5)

    plt.tight_layout()
    plt.savefig(mapa_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"[MAPPING] Prancha cartográfica gerada com shapefile real: {mapa_path}")
    return mapa_path
