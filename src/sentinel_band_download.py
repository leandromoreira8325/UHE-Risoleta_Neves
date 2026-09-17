"""
sentinel_band_download.py

Download direto das bandas Sentinel-2
utilizando os links STAC.
"""

from pathlib import Path

import requests

from src.config import DATA_DIR
from src.copernicus_api import CopernicusDataSpaceAPI


def baixar_banda(
    url: str,
    nome_arquivo: str
) -> Path:

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    destino = (
        DATA_DIR /
        nome_arquivo
    )

    api = CopernicusDataSpaceAPI()

    token = api.obter_token()

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    print(
        f"[DOWNLOAD] {nome_arquivo}"
    )

    response = requests.get(
        url,
        headers=headers,
        stream=True,
        timeout=300
    )

    response.raise_for_status()

    with open(
        destino,
        "wb"
    ) as arquivo:

        for chunk in response.iter_content(
            chunk_size=8192
        ):

            if chunk:

                arquivo.write(
                    chunk
                )

    print(
        f"[DOWNLOAD] Salvo:"
    )

    print(
        destino
    )

    return destino


def baixar_bandas_principais(
    cena: dict
) -> dict:

    arquivos = {}

    arquivos["B03"] = baixar_banda(
        cena["B03"],
        "B03_10m.jp2"
    )

    arquivos["B04"] = baixar_banda(
        cena["B04"],
        "B04_10m.jp2"
    )

    arquivos["B08"] = baixar_banda(
        cena["B08"],
        "B08_10m.jp2"
    )

    arquivos["SCL"] = baixar_banda(
        cena["SCL"],
        "SCL_20m.jp2"
    )

    return arquivos
