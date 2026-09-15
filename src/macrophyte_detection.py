"""
macrophyte_detection.py

Detecção de macrófitas utilizando
NDVI + Máscara de Água.

UHE Risoleta Neves
"""

import numpy as np
import rasterio

from src.config import NDVI_THRESHOLD


def calcular_ndvi(
    banda_red: str,
    banda_nir: str,
    output_ndvi: str
) -> str:
    """
    NDVI = (NIR - RED) / (NIR + RED)

    Sentinel-2:
    B4 = Red
    B8 = NIR
    """

    with rasterio.open(banda_red) as red_src:

        red = red_src.read(1).astype("float32")

        profile = red_src.profile.copy()

    with rasterio.open(banda_nir) as nir_src:

        nir = nir_src.read(1).astype("float32")

    np.seterr(divide="ignore")

    ndvi = (
        (nir - red)
        /
        (nir + red)
    )

    ndvi = np.where(
        np.isnan(ndvi),
        -9999,
        ndvi
    )

    profile.update(
        dtype=rasterio.float32,
        nodata=-9999,
        compress="lzw"
    )

    with rasterio.open(
        output_ndvi,
        "w",
        **profile
    ) as dst:

        dst.write(
            ndvi.astype(
                rasterio.float32
            ),
            1
        )

    print(
        f"[NDVI] Gerado: {output_ndvi}"
    )

    return output_ndvi


def detectar_macrofitas(
    ndvi_path: str,
    water_mask_path: str,
    output_raster: str
) -> str:
    """
    Detecta macrófitas:

  
