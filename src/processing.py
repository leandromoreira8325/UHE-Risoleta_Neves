import rasterio
from rasterio.mask import mask
import numpy as np
import geopandas as gpd

def calcular_area_macrophitas_real(raster_path, shapefile_path):
    """
    Calcula o percentual de área de macrófitas com base nos pixels reais do Sentinel-2
    mascarados pela poligonal do reservatório.
    """
    # Carrega a poligonal
    gdf = gpd.read_file(shapefile_path)
    
    with rasterio.open(raster_path) as src:
        # Recorta o raster usando a geometria do shapefile do reservatório
        out_image, out_transform = mask(src, gdf.geometry, crop=True)
        
        # Exemplo com bandas multiespectrais reais (ex: Banda 8 = NIR, Banda 4 = Red)
        # NDVI = (NIR - Red) / (NIR + Red)
        # Supondo que out_image[3] seja NIR e out_image[2] seja Red (padrão Sentinel-2 L2A)
        red = out_image[2].astype(float)
        nir = out_image[3].astype(float)
        
        # Evita divisão por zero
        denominator = (nir + red)
        denominator[denominator == 0] = 0.0001
        ndvi = (nir - red) / denominator
        
        # Máscara de pixels válidos dentro do corpo d'água/reservatório (removendo no-data)
        valid_pixels = out_image[0] != src.nodata
        ndvi_valid = ndvi[valid_pixels]
        
        # Limiar típico para detecção de macrófitas densas/vegetação aquática flutuante (NDVI entre 0.25 e 0.6)
        macrophita_pixels = np.sum((ndvi_valid >= 0.25) & (ndvi_valid <= 0.65))
        total_pixels = np.sum(valid_pixels)
        
        if total_pixels > 0:
            percentual = (macrophita_pixels / total_pixels) * 100
        else:
            percentual = 0.0
            
        return percentual
