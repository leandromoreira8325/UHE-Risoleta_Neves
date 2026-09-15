"""
config.py

Configurações globais do projeto
UHE Risoleta Neves - Monitoramento de Macrófitas
"""

from pathlib import Path

# =====================================================================
# ESTRUTURA DE DIRETÓRIOS
# =====================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "outputs"

DATA_DIR = BASE_DIR / "data"

LOG_DIR = BASE_DIR / "logs"

# =====================================================================
# SHAPEFILE OFICIAL
# =====================================================================

SHAPEFILE_PATH = (
    BASE_DIR /
    "UHE_Risoleta_Neves_Reservatorio.shp"
)

# =====================================================================
# DADOS DO RESERVATÓRIO
# =====================================================================

AREA_OFICIAL_HA = 1450.00

# =====================================================================
# PARÂMETROS DE AQUISIÇÃO SENTINEL-2
# =====================================================================

DATA_INICIAL = "2026-01-01"

DATA_FINAL = "2026-12-31"

NUVEM_MAXIMA = 10

SATELITE = "Sentinel-2 MSI"

# =====================================================================
# PROCESSAMENTO
# =====================================================================

PIXEL_SIZE = 10

CRS_PADRAO = "EPSG:4326"

# =====================================================================
# MACRÓFITAS
# =====================================================================

NDVI_THRESHOLD = 0.20

NDWI_THRESHOLD = 0.05

FAI_THRESHOLD = 0.005

# =====================================================================
# ESTIMATIVA DE VOLUME RETIDO
# =====================================================================

ESPESSURA_MEDIA_M = 0.35

FATOR_RETENCAO = 0.65

# =====================================================================
# CRIAÇÃO AUTOMÁTICA DOS DIRETÓRIOS
# =====================================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)
