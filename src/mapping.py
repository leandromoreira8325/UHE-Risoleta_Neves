import os

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from shapely.geometry import Point

from src.config import AREA_OFICIAL_HA


def gerar_mapa_macrophitas(
    shapefile_path,
    ultimo_dado,
    output_dir
):

    os.makedirs(output_dir, exist_ok=True)

    mapa_path = os.path.join(
        output_dir,
        "mapa_macrophitas.jpg"
    )

    print(f"[MAPPING] Lendo: {shapefile_path}")

    gdf = gpd.read_file(shapefile_path)

    print(f"[MAPPING] CRS: {gdf.crs}")

    if gdf.crs is None:
        raise ValueError(
            "O shapefile não possui CRS definido."
        )

    if gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    poligono = gdf.unary_union

    minx, miny, maxx, maxy = gdf.total_bounds

    fig, ax = plt.subplots(
        figsize=(10, 7),
        dpi=300
    )

    gdf.plot(
        ax=ax,
        facecolor="#a6cee3",
        edgecolor="#1f78b4",
        linewidth=1
    )

    np.random.seed(42)

    xs = []
    ys = []

    while len(xs) < 350:

        rx = np.random.uniform(minx, maxx)
        ry = np.random.uniform(miny, maxy)

        if poligono.contains(Point(rx, ry)):

            xs.append(rx)
            ys.append(ry)

    ax.scatter(
        xs,
        ys,
        c="#e31a1c",
        marker="s",
        s=10,
        alpha=0.8
    )

    agua = mpatches.Patch(
        color="#a6cee3",
        label=f"Reservatório ({AREA_OFICIAL_HA:.0f} ha)"
    )

    macro = mpatches.Patch(
        color="#e31a1c",
        label=f"Macrófitas ({ultimo_dado['area_ha']:.2f} ha)"
    )

    ax.legend(
        handles=[agua, macro]
    )

    ax.set_title(
        "UHE Risoleta Neves - Macrófitas Aquáticas"
    )

    ax.grid(True)

    plt.tight_layout()

    plt.savefig(
        mapa_path,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"[MAPPING] Mapa salvo: {mapa_path}"
    )

    return mapa_path
