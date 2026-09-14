"""
Script Principal - Automação de Monitoramento de Macrófitas
"""
import os
from src.config import OUTPUT_DIR, UHE_NOME, AREA_OFICIAL_AGUA_HA, SHAPEFILE_RESERVATORIO
from src.processing import processar_serie_temporal
from src.report import gerar_relatorio_pdf

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"--- Iniciando monitoramento para: {UHE_NOME} ---")
    
    # Processa as cenas e métricas
    dados_mensais = processar_serie_temporal(
        shapefile_path=SHAPEFILE_RESERVATORIO,
        output_dir=OUTPUT_DIR
    )
    
    # Gera o relatório PDF consolidado
    gerar_relatorio_pdf(
        dados=dados_mensais,
        output_dir=OUTPUT_DIR,
        area_oficial_ha=AREA_OFICIAL_AGUA_HA
    )
    
    print("[FLUXO CONCLUÍDO] Processamento finalizado com sucesso.")

if __name__ == "__main__":
    main()
