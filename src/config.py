"""
config.py

Configurações globais do projeto
UHE Risoleta Neves
"""

from pathlib import Path


# =====================================================
# DIRETÓRIO BASE
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# DIRETÓRIOS DE SAÍDA
# =====================================================

OUTPUT_DIR = BASE_DIR / "outputs"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# SHAPEFILE OFICIAL
# =====================================================

SHAPEFILE_PATH = (
    BASE_DIR /
    "UHE_Risoleta_Neves_Reservatorio.shp"
)


# =====================================================
# RESERVATÓRIO
# =====================================================

AREA_OFICIAL_HA = 1450.0


# =====================================================
# SENTINEL-2
# =====================================================

DATA_INICIAL = "2026-01-01"
DATA_FINAL = "2026-12-31"

NUVEM_MAXIMA = 10

SATELITE = "Sentinel-2 MSI"


# =====================================================
# PROCESSAMENTO
# =====================================================

CRS_PADRAO = "EPSG:4326"

PIXEL_SIZE = 10


# =====================================================
# ÍNDICES ESPECTRAIS
# =====================================================

NDWI_THRESHOLD = 0.05
NDVI_THRESHOLD = 0.20
FAI_THRESHOLD = 0.005


# =====================================================
# VOLUME RETIDO
# =====================================================

ESPESSURA_MEDIA_M = 0.35
FATOR_RETENCAO = 0.65
