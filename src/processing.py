"""
processing.py

Fluxo principal de processamento.
"""

from pathlib import Path

from src.config import (
    SHAPEFILE_PATH,
    OUTPUT_DIR,
    AREA_OFICIAL_HA
)

from src.sentinel_search import buscar_melhor_cena

from src.raster_processing import preparar_bandas

from src.water_mask import (
    calcular_ndwi,
    gerar_mascara_agua
)

from src.macrophyte_detection import (
    calcular_ndvi,
    detectar_macrofitas
)

from src.area_calculation import (
    calcular_area_macrofitas
)


def processar_dados_2026():

    print("[PROCESSING] Iniciando processamento...")

    cena = buscar_melhor_cena()

    if cena is None:

        raise RuntimeError(
            "Nenhuma cena Sentinel encontrada."
        )

    base_data = Path("data")

    banda_b3 = base_data / "B3.tif"
    banda_b4 = base_data / "B4.tif"
    banda_b8 = base_data / "B8.tif"

    if not banda_b3.exists():
        raise FileNotFoundError(
            "Arquivo data/B3.tif não encontrado."
        )

    if not banda_b4.exists():
        raise FileNotFoundError(
            "Arquivo data/B4.tif não encontrado."
        )

    if not banda_b8.exists():
        raise FileNotFoundError(
            "Arquivo data/B8.tif não encontrado."
        )

    bandas = preparar_bandas(
        str(banda_b3),
        str(banda_b8),
        str(OUTPUT_DIR)
    )

    ndwi_path = OUTPUT_DIR / "ndwi.tif"

    calcular_ndwi(
        bandas["B3"],
        bandas["B8"],
        str(ndwi_path)
    )

    water_mask_path = (
        OUTPUT_DIR /
        "water_mask.tif"
    )

    gerar_mascara_agua(
        str(ndwi_path),
        str(water_mask_path)
    )

    ndvi_path = (
        OUTPUT_DIR /
        "ndvi.tif"
    )

    calcular_ndvi(
        str(banda_b4),
        str(banda_b8),
        str(ndvi_path)
    )

    macrofitas_path = (
        OUTPUT_DIR /
        "macrofitas.tif"
    )

    detectar_macrofitas(
        str(ndvi_path),
        str(water_mask_path),
        str(macrofitas_path)
    )

    resultado = calcular_area_macrofitas(
        str(macrofitas_path)
    )

    area_ha = resultado["area_ha"]

    percentual = (
        area_ha
        /
        AREA_OFICIAL_HA
    ) * 100

    dados_serie = [
        {
            "mes": str(
                cena["data"]
            )[:10],

            "area_ha": round(
                area_ha,
                2
            ),

            "percentual": round(
                percentual,
                2
            ),

            "status": (
                f"Sentinel-2 "
                f"({cena['nuvens']}% nuvens)"
            )
        }
    ]

    print(
        f"[PROCESSING] Área encontrada: "
        f"{area_ha:.2f} ha"
    )

    return (
        dados_serie,
        str(SHAPEFILE_PATH)
    )
