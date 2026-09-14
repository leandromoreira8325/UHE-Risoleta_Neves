import os

# Configurações do Reservatório da UHE Risoleta Neves (Candonga)
AREA_OFICIAL_HA = 1450.0  # Área oficial do reservatório em hectares

# Diretórios do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
DATA_DIR = os.path.join(BASE_DIR, 'data')
