"""
area_calculation.py

Cálculo de área de macrófitas.
"""

import numpy as np
import rasterio


def calcular_area_macrofitas(
    macrofitas_raster: str,
    pixel_size: float = 10.0
):
    """
    Calcula área ocupada por macrófitas.

    Sentinel-2:
        10 m x 10 m = 100 m²
    """

    with rasterio.open(
        macrofitas_raster
    ) as src:

        dados = src.read(1)

    pixels_macrofitas = np.sum(
        dados == 1
    )

    area_m2 = (
        pixels_macrofitas
        * pixel_size
        * pixel_size
    )

    area_ha = (
        area_m2
        / 10000
    )

    return {
        "pixels": int(
            pixels_macrofitas
        ),
        "area_m2": float(
            area_m2
        ),
        "area_ha": float(
            area_ha
        )
    }
