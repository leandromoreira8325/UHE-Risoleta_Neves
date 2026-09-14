"""
Script Principal - Automação de Monitoramento de Macrófitas
"""
import os
from src import config
from src.processing import processar_serie_temporal
from src.report import gerar_relatorio_pdf

def main():
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    print(f"--- Iniciando monitoramento para: {config.UHE_NOME} ---")
    
    # Processa as cenas e métricas
    dados_mensais = processar_serie_temporal(
        shapefile_path=config.SHAPEFILE_RESERVATORIO,
        output_dir=config.OUTPUT_DIR
    )
    
    # Gera o relatório PDF consolidado
    gerar_relatorio_pdf(
        dados=dados_mensais,
        output_dir=config.OUTPUT_DIR,
        area_oficial_ha=config.AREA_OFICIAL_AGUA_HA
    )
    
    print("[FLUXO CONCLUÍDO] Processamento finalizado com sucesso.")

if __name__ == "__main__":
    main()
