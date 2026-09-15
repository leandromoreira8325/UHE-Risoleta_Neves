"""
raster_processing.py

Processamento de rasters Sentinel-2.

Responsável por:
- Abrir bandas
- Validar CRS
- Recortar pelo reservatório
- Salvar bandas preparadas para NDWI
"""

from pathlib import Path

import geopandas as gpd
import rasterio
from rasterio.mask import mask

from src.config import SHAPEFILE_PATH


def recortar_banda(
    raster_path: str,
    output_path: str
) -> str:
    """
    Recorta uma banda raster utilizando
    a poligonal do reservatório.
    """

    gdf = gpd.read_file(SHAPEFILE_PATH)

    with rasterio.open(raster_path) as src:

        if gdf.crs != src.crs:
            gdf = gdf.to_crs(src.crs)

        geometrias = [
            geom
            for geom in gdf.geometry
        ]

        raster_clipado, transform = mask(
            src,
            geometrias,
            crop=True
        )

        metadata = src.meta.copy()

    metadata.update(
        {
            "height": raster_clipado.shape[1],
            "width": raster_clipado.shape[2],
            "transform": transform
        }
    )

    with rasterio.open(
        output_path,
        "w",
        **metadata
    ) as dst:

        dst.write(
            raster_clipado
        )

    print(
        f"[RASTER] Banda recortada: "
        f"{output_path}"
    )

    return output_path


def preparar_bandas(
    banda_b3: str,
    banda_b8: str,
    output_dir: str
):
    """
    Prepara as bandas necessárias
    para o cálculo do NDWI.
    """

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    b3_clip = output_dir / "B3_clip.tif"

    b8_clip = output_dir / "B8_clip.tif"

    recortar_banda(
        banda_b3,
        str(b3_clip)
    )

    recortar_banda(
        banda_b8,
        str(b8_clip)
    )

    return {
        "B3": str(b3_clip),
        "B8": str(b8_clip)
    }
