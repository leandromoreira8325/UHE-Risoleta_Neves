from src.processing import processar_serie_temporal_2026
from src.mapping import gerar_mapa_macrophitas
from src.report import gerar_relatorio_pdf
from src.config import AREA_OFICIAL_HA, OUTPUT_DIR
import glob

if __name__ == "__main__":
    print("--- Iniciando Pipeline de Monitoramento Ambiental: UHE Risoleta Neves ---")
    
    # 1. Processa a série histórica e busca as cenas do Copernicus
    dados_serie, imagens_2026 = processar_serie_temporal_2026()
    
    # 2. Localiza o shapefile oficial na raiz para gerar o mapa espacial
    shape_files = glob.glob("*UHE_Risoleta_Neves_Reservatorio.shp") + glob.glob("**/*UHE_Risoleta_Neves_Reservatorio.shp", recursive=True)
    if shape_files:
        shapefile_path = shape_files[0]
        print("[PROCESSING] Gerando mapa cartográfico do reservatório...")
        mapa_path = gerar_mapa_macrophitas(shapefile_path, OUTPUT_DIR)
    else:
        print("[AVISO] Shapefile não encontrado para gerar o mapa. O relatório será gerado apenas com a tabela.")
        mapa_path = None

    # 3. Compila o relatório em PDF consolidado usando AREA_OFICIAL_HA corretos
    gerar_relatorio_pdf(dados_serie, imagens_2026, OUTPUT_DIR, AREA_OFICIAL_HA, mapa_path)
    
    print("Pipeline executado com sucesso! Relatório e mapa gerados na pasta outputs/.")
