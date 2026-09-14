"""
Configurações e parâmetros para o monitoramento da UHE Risoleta Neves.
"""

# Identificação da Usina
UHE_NOME = "UHE Risoleta Neves (Candonga)"
AREA_OFICIAL_AGUA_HA = 1450.00  # Ajuste aqui o valor exato do espelho d'água oficial se necessário

# Caminhos de arquivos
SHAPEFILE_RESERVATORIO = "data/limite_reservatorio.geojson"
OUTPUT_DIR = "outputs"

# Parâmetros de Processamento
BUFFER_MARGEM_METROS = -12.0  # Isola ruídos de borda e vegetação marginal
INDICE_ALERTA_HA = 150.00     # Limite de referência para alerta de macrófitas
