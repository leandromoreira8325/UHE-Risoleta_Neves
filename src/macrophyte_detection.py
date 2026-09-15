"""
macrophyte_detection.py

Detecção de macrófitas utilizando
NDVI + Máscara de Água.
"""

import numpy as np
import rasterio

from src.config import NDVI_THRESHOLD


def calcular_ndvi(
    banda_red: str,
    banda_nir: str,
    output_ndvi: str
) -> str:

    with rasterio.open(banda_red) as red_src:

        red = red_src.read(1).astype("float32")

        profile = red_src.profile.copy()

    with rasterio.open(banda_nir) as nir_src:

        nir = nir_src.read(1).astype("float32")

    np.seterr(divide="ignore")

    ndvi = (nir - red) / (nir + red)

    ndvi = np.where(
        np.isnan(ndvi),
        -9999,
        ndvi
    )

    profile.update(
        dtype=rasterio.float32,
        nodata=-9999
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

    return output_ndvi


def detectar_macrofitas(
    ndvi_path: str,
    water_mask_path: str,
    output_raster: str
) -> str:

    with rasterio.open(
        ndvi_path
    ) as ndvi_src:

        ndvi = ndvi_src.read(1)

        profile = ndvi_src.profile.copy()

    with rasterio.open(
        water_mask_path
    ) as water_src:

        water_mask = water_src.read(1)

    macrofitas = np.where(
        (water_mask == 1)
        &
        (ndvi > NDVI_THRESHOLD),
        1,
        0
    )

    profile.update(
        dtype=rasterio.uint8,
        nodata=0
    )

    with rasterio.open(
        output_raster,
        "w",
        **profile
    ) as dst:

        dst.write(
            macrofitas.astype(
                rasterio.uint8
            ),
            1
        )

    return output_raster
