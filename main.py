from src.processing import processar_serie_temporal_2026
from src.report import gerar_relatorio_pdf
from src.config import AREA_OFICIAL_HA, OUTPUT_DIR

if __name__ == "__main__":
    print("--- Iniciando Pipeline de Monitoramento Ambiental: UHE Risoleta Neves ---")
    
    # Processa os dados espaciais e a série histórica
    dados_serie, imagens_2026 = processar_serie_temporal_2026()
    
    # Compila o relatório em PDF consolidado
    gerar_relatorio_pdf(dados_serie, imagens_2026, OUTPUT_DIR, AREA_OFICIAL_HA)
    
    print("Pipeline executado com sucesso! Relatório gerado na pasta outputs/.")
