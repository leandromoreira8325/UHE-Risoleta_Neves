import os

# Raiz do repositório (um nível acima da pasta src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AREA_OFICIAL_HA = 1450.0
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
SHAPEFILE_PATH = os.path.join(BASE_DIR, "UHE_Risoleta_Neves_Reservatorio.shp")
