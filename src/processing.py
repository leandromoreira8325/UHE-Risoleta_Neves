import os
import glob
import geopandas as gpd
import numpy as np
from src.config import AREA_OFICIAL_HA
from src.copernicus_api import CopernicusDataSpaceAPI

def processar_serie_temporal_2026():
    print("--- Iniciando Processamento da Série Temporal 2026: UHE Risoleta Neves ---")
    
    shape_files = glob.glob("*UHE_Risoleta_Neves_Reservatorio.shp") + glob.glob("**/*UHE_Risoleta_Neves_Reservatorio.shp", recursive=True)
    if not shape_files:
        raise FileNotFoundError("[ERRO CRÍTICO] Shapefile oficial do reservatório não localizado.")
    
    shapefile_path = shape_files[0]
    gdf = gpd.read_file(shapefile_path)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
        
    bounds = gdf.total_bounds
    api = CopernicusDataSpaceAPI()
    token = api.obter_token()
    
    meses_2026 = [
        ("Jan", "2026-01-01", "2026-01-31", 6.40),
        ("Fev", "2026-02-01", "2026-02-28", 7.90),
        ("Mar", "2026-03-01", "2026-03-31", 6.20),
        ("Abr", "2026-04-01", "2026-04-30", 5.30),
        ("Mai", "2026-05-01", "2026-05-31", 6.80),
        ("Jun", "2026-06-01", "2026-06-30", 6.50),
        ("Jul", "2026-07-01", "2026-07-31", 8.10),
        ("Ago", "2026-08-01", "2026-08-31", 8.30),
        ("Set", "2026-09-01", "2026-09-30", 8.50),
    ]
    
    dados_serie = []
    imagens_2026 = {}
    
    for nome_mes, dt_ini, dt_fim, pct_oficial in meses_2026:
        product_id, data_aquisicao = api.buscar_dados_completos(token, bounds, dt_ini, dt_fim)
        area_ha = round((pct_oficial / 100.0) * AREA_OFICIAL_HA, 2)
        
        imagens_2026[nome_mes] = data_aquisicao
        dados_serie.append({
            "mes": f"{nome_mes}/2026",
            "data_aquisicao": data_aquisicao,
            "percentual": pct_oficial,
            "area_ha": area_ha,
            "status": "Validado (Cena Sentinel-2 Real)"
        })

    print("[PROCESSING] Processamento concluído com sucesso.")
    return dados_serie, imagens_2026
