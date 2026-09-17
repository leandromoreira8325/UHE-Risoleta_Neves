import os
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def gerar_mapa_macrophitas(shapefile_path, ultimo_dado, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    mapa_path = os.path.join(output_dir, "mapa_macrophitas.jpg")

    # 1. Localização estrita do arquivo .shp
    base_dir = Path(__file__).resolve().parent.parent
    candidatos = list(base_dir.glob("*.shp")) + list(base_dir.glob("data/*.shp")) + list(base_dir.glob("*.[sS][hH][pP]"))
    
    if not candidatos:
        raise FileNotFoundError(
            f"[ERRO CRÍTICO] Nenhum arquivo .shp encontrado em '{base_dir}'. "
            "Certifique-se de que os arquivos do shapefile (.shp, .shx, .dbf, .prj) foram enviados ao repositório."
        )
    
    target_shp = candidatos[0]
    print(f"[MAPPING] Renderizando geometria real do vetor: {target_shp}")

    # 2. Carregamento direto da geometria real sem simplificação
    gdf = gpd.read_file(target_shp)
    if gdf.crs is None or str(gdf.crs).lower() != "epsg:4326":
        gdf = gdf.to_crs("EPSG:4326")

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    
    # 3. Desenho direto do GeoDataFrame real (espelho d'água original)
    gdf.plot(
        ax=ax, 
        facecolor='#a6cee3', 
        edgecolor='#1f78b4', 
        linewidth=0.6, 
        alpha=0.85, 
        zorder=1
    )

    area_ha = ultimo_dado.get("area_ha", 0.0)
    pct = ultimo_dado.get("percentual", 0.0)

    # 4. Legendas e Acabamento Cartográfico
    AREA_OFICIAL_HA = 1450.0
    patch_agua = mpatches.Patch(
        color='#a6cee3', 
        ec='#1f78b4', 
        label=f"Reservatório ({AREA_OFICIAL_HA:,.0f} ha)".replace(',', '.')
    )
    patch_macro = mpatches.Patch(
        color='#e31a1c', 
        label=f"Macrófitas ({area_ha:.2f} ha - {pct:.2f}%)"
    )

    ax.set_title("UHE Risoleta Neves - Macrófitas Aquáticas", fontsize=11, fontweight='bold', pad=12)
    ax.set_xlabel("Longitude (WGS84)", fontsize=8.5)
    ax.set_ylabel("Latitude (WGS84)", fontsize=8.5)
    ax.grid(True, linestyle=':', alpha=0.4, zorder=0)
    ax.legend(handles=[patch_agua, patch_macro], loc='upper right', framealpha=0.95, edgecolor='gray', fontsize=8.5)

    # Enquadramento automático no bounding box exato da geometria real
    minx, miny, maxx, maxy = gdf.total_bounds
    margin_x = (maxx - minx) * 0.03
    margin_y = (maxy - miny) * 0.03
    ax.set_xlim([minx - margin_x, maxx + margin_x])
    ax.set_ylim([miny - margin_y, maxy + margin_y])

    plt.tight_layout()
    plt.savefig(mapa_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[MAPPING] Prancha cartográfica atualizada com geometria real: {mapa_path}")
    return mapa_path
