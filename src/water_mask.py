"""
water_mask.py

Geração de NDWI e máscara de água.

Projeto:
Monitoramento de Macrófitas
UHE Risoleta Neves

Autor:
Leandro Alves Moreira
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import rasterio


def calcular_ndwi(
    banda_green: str,
    banda_nir: str,
    output_ndwi: str
) -> str:
    """
    Calcula NDWI.

    NDWI = (Green - NIR) / (Green + NIR)

    Parameters
    ----------
    banda_green : str
        Banda B3 Sentinel-2.

    banda_nir : str
        Banda B8 Sentinel-2.

    output_ndwi : str
        Arquivo de saída.

    Returns
    -------
    str
    """

    with rasterio.open(banda_green) as green_src:

        green = green_src.read(1).astype("float32")

        profile = green_src.profile.copy()

    with rasterio.open(banda_nir) as nir_src:

        nir = nir_src.read(1).astype("float32")

    np.seterr(divide="ignore")

    ndwi = (
        (green - nir)
        /
        (green + nir)
    )

    ndwi = np.where(
        np.isnan(ndwi),
        -9999,
        ndwi
    )

    profile.update(
        dtype=rasterio.float32,
        nodata=-9999,
        compress="lzw"
    )

    with rasterio.open(
        output_ndwi,
        "w",
        **profile
    ) as dst:

        dst.write(
            ndwi.astype(
                rasterio.float32
            ),
            1
        )

    print(
        f"[NDWI] Arquivo gerado: "
        f"{output_ndwi}"
    )

    return output_ndwi


def gerar_mascara_agua(
    ndwi_path: str,
    output_mask: str,
    threshold: float = 0.05
) -> str:
    """
    Gera máscara binária de água.

    Parameters
    ----------
    ndwi_path : str

    output_mask : str

    threshold : float

    Returns
    -------
    str
    """

    with rasterio.open(
        ndwi_path
    ) as src:

        ndwi = src.read(1)

        profile = src.profile.copy()

    mask = np.where(
        ndwi > threshold,
        1,
        0
    )

    profile.update(
        dtype=rasterio.uint8,
        nodata=0,
        compress="lzw"
    )

    with rasterio.open(
        output_mask,
        "w",
        **profile
    ) as dst:

        dst.write(
            mask.astype(
                rasterio.uint8
            ),
            1
        )

    print(
        f"[WATER MASK] "
        f"Arquivo gerado: "
        f"{output_mask}"
    )

    return output_mask


if __name__ == "__main__":

    print(
        "Módulo de NDWI carregado."
    )
