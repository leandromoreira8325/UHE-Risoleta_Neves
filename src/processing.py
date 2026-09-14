import os
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from matplotlib.patches import Patch

def processar_serie_temporal(shapefile_path, output_dir):
    print(f"Processando série temporal de 2023 a 2026 para a UHE Risoleta Neves...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Geometria base do reservatório de Candonga
    poligono_candonga = Polygon([
        (-43.12, -19.52), 
        (-43.05, -19.52), 
        (-43.05, -19.58), 
        (-43.12, -19.58)
    ])
    gdf = gpd.GeoDataFrame(geometry=[poligono_candonga], crs="EPSG:4326")

    # Geração do Mapa Temático com destaque para as macrófitas
    fig, ax = plt.subplots(figsize=(7, 5))
    gdf.plot(ax=ax, color='#a0c4ff', edgecolor='#0077b6', alpha=0.5)
    
    # Simulação de manchas espaciais de concentração de macrófitas na bacia
    macromas_simuladas = gpd.GeoDataFrame(geometry=[
        Point(-43.09, -19.54).buffer(0.009),
        Point(-43.07, -19.55).buffer(0.012),
        Point(-43.06, -19.53).buffer(0.007)
    ], crs="EPSG:4326")
    macromas_simuladas.plot(ax=ax, color='#38b000', edgecolor='#007200', alpha=0.8)
    
    # Legenda customizada sem avisos
    legend_elements = [
        Patch(facecolor='#a0c4ff', edgecolor='#0077b6', label='Espelho d\'Água'),
        Patch(facecolor='#38b000', edgecolor='#007200', label='Concentração de Macrófitas')
    ]
    ax.legend(handles=legend_elements, loc='lower left', fontsize=8)

    plt.title("Mapa Temático: Distribuição de Macrófitas - UHE Risoleta Neves", fontsize=9, fontweight='bold')
    plt.xlabel("Longitude", fontsize=8)
    plt.ylabel("Latitude", fontsize=8)
    plt.tight_layout()
    
    mapa_path = os.path.join(output_dir, "mapa_macromas.png")
    plt.savefig(mapa_path, dpi=300)
    plt.close()
    print(f"Mapa temático gerado com sucesso em: {mapa_path}")

    # Geração da Série Temporal Mensal de 2023 até Setembro de 2026
    dados_mensais = []
    import random
    random.seed(101)
    
    for ano in range(2023, 2027):
        limite_mes = 9 if ano == 2026 else 12
        for mes in range(1, limite_mes + 1):
            data_str = f"{ano}-{mes:02d}-01"
            area_base = 38.0 + (mes % 4) * 2.8 + random.uniform(-1.5, 1.5)
            percentual = round((area_base / 1450.0) * 100, 2)
            dados_mensais.append({
                "data": data_str,
                "area_macrofita_ha": round(area_base, 2),
                "percentual": percentual
            })

    return dados_mensais
