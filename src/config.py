import os
from pathlib import Path

# Localiza a raiz do repositório (um nível acima de src/)
BASE_DIR = Path(__file__).resolve().parent.parent

AREA_OFICIAL_HA = 1450.0
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Caminho absoluto para o Shapefile na raiz
SHAPEFILE_PATH = os.path.join(BASE_DIR, "UHE_Risoleta_Neves_Reservatorio.shp")
