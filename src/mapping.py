import os
import glob
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from rasterio.plot import show
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap

def gerar_prancha_tematica(shapefile_path, raster_path, output_dir, mes_nome, area_total, area_macrofita):
    """
    Gera o mapa temático real sobrepondo a matriz de pixels classificados 
    (raster Sentinel-2) sobre a geometria do shapefile da usina.
    """
    os.makedirs(output_dir, exist_ok=True)
    mapa_path = os.path.join(output_dir, f"mapa_2026_{mes_nome}.png")
    
    # 1. Carrega e prepara o Shapefile (Poligonal do Reservatório)
    gdf = gpd.read_file(shapefile_path)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    
    # 2. Configura a prancha cartográfica
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plota o espelho d'água oficial (Base Azul)
    gdf.plot(ax=ax, color='#b3cde3', edgecolor='#1f78b4', linewidth=1.5)
    
    # 3. Processamento Real do Raster (Imagem de Satélite Classificada)
    try:
        with rasterio.open(raster_path) as src:
            # Recorta a imagem de satélite exatamente nos limites do shapefile
            out_image, out_transform = rasterio.mask.mask(src, gdf.geometry, crop=True)
            out_meta = src.meta
            
            # Assume-se que o raster contém a máscara binária: 1 = Macrófita, 0 = Água/Nuvem
            matriz_pixels = out_image[0]
            
            # Cria um Colormap onde 0 (fundo) é transparente e 1 (macrófita) é vermelho
            cmap_macrofita = ListedColormap(['none', 'red'])
            
            # Calcula a extensão espacial correta para alinhar os pixels ao shapefile
            extensao = [
                out_transform[2],
                out_transform[2] + out_transform[0] * matriz_pixels.shape[1],
                out_transform[5] + out_transform[4] * matriz_pixels.shape[0],
                out_transform[5]
            ]
            
            # Plota OS PIXELS REAIS detectados por sensoriamento remoto
            ax.imshow(matriz_pixels, cmap=cmap_macrofita, extent=extensao, interpolation='none', alpha=0.9)
            
    except Exception as e:
        print(f"[AVISO MAPPING] Arquivo Raster não encontrado ou inválido: {raster_path}. Erro: {e}")
        # Retorno de segurança caso o TIF falhe, mantendo a geração do PDF
        pass

    # 4. Legendas e Acabamento (Idêntico ao padrão Aimorés)
    patch_agua = mpatches.Patch(color='#b3cde3', ec='#1f78b4', label=f"Espelho d'Água ({area_total:.2f} ha)")
    patch_macro = mpatches.Patch(color='red', label=f"Macrófitas Detectadas ({area_macrofita:.2f} ha)")

    titulo = f"PRANCHA TEMÁTICA DE MACRÓFITAS - UHE RISOLETA NEVES ({mes_nome.upper()}/2026)"
    ax.set_title(titulo, fontsize=12, fontweight='bold', pad=15)
    ax.set_xlabel("Longitude (WGS84)", fontsize=10)
    ax.set_ylabel("Latitude (WGS84)", fontsize=10)
    
    # Grid e Legenda
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(handles=[patch_agua, patch_macro], loc='upper right', framealpha=1, edgecolor='gray', fontsize=10)
    
    # Ajusta os limites do gráfico para focar no shapefile
    bounds = gdf.total_bounds
    ax.set_xlim([bounds[0] - 0.005, bounds[2] + 0.005])
    ax.set_ylim([bounds[1] - 0.005, bounds[3] + 0.005])
    
    plt.tight_layout()
    plt.savefig(mapa_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return mapa_path
