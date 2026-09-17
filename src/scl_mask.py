"""
scl_mask.py

Máscara de nuvens e sombras
Sentinel-2 L2A SCL.
"""

import numpy as np
import rasterio


def gerar_mascara_scl(
    scl_raster: str,
    output_mask: str
):

    with rasterio.open(
        scl_raster
    ) as src:

        scl = src.read(1)

        profile = src.profile.copy()

    classes_ruido = [
        3,   # cloud shadow
        8,   # cloud medium probability
        9,   # cloud high probability
        10,  # cirrus
        11   # snow
    ]

    mascara = np.where(
        np.isin(
            scl,
            classes_ruido
        ),
        0,
        1
    )

    profile.update(
        dtype=rasterio.uint8,
        nodata=0
    )

    with rasterio.open(
        output_mask,
        "w",
        **profile
    ) as dst:

        dst.write(
            mascara.astype(
                rasterio.uint8
            ),
            1
        )

    print(
        f"[SCL] Máscara salva: "
        f"{output_mask}"
    )

    return output_mask
