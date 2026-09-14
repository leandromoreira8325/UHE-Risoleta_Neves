import glob
from src.processing import processar_serie_temporal_2026
from src.mapping import gerar_mapa_macrophitas
from src.report import gerar_relatorio_pdf
from src.config import AREA_OFICIAL_HA, OUTPUT_DIR

if __name__ == "__main__":
    print("--- Iniciando Pipeline de Monitoramento Ambiental: UHE Risoleta Neves ---")
    
    # 1. Executa o processamento analítico e captura as cenas orbitais reais
    dados_serie, imagens_2026 = processar_serie_temporal_2026()
    
    # 2. Localiza o shapefile oficial para o mapeamento espacial cartográfico
    shape_files = glob.glob("*UHE_Risoleta_Neves_Reservatorio.shp") + glob.glob("**/*UHE_Risoleta_Neves_Reservatorio.shp", recursive=True)
    if shape_files:
        shapefile_path = shape_files[0]
        print("[PROCESSING] Gerando mapa cartográfico baseado na poligonal oficial...")
        mapa_path = gerar_mapa_macrophitas(shapefile_path, OUTPUT_DIR)
    else:
        print("[AVISO CRÍTICO] Shapefile não localizado para geração do mapa vetorial.")
        mapa_path = None

    # 3. Compila o relatório executivo oficial em PDF
    gerar_relatorio_pdf(dados_serie, imagens_2026, OUTPUT_DIR, AREA_OFICIAL_HA, mapa_path)
    
    print("Pipeline executado com total integridade! Relatório e mapa auditáveis salvos na pasta 'outputs/'.")
