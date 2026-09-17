"""
sentinel_download.py

Download direto das bandas Sentinel-2.
"""

from pathlib import Path

import requests

from src.config import DATA_DIR
from src.copernicus_api import CopernicusDataSpaceAPI


def baixar_banda(
    url: str,
    nome_arquivo: str
):

    api = CopernicusDataSpaceAPI()

    token = api.obter_token()

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    destino = (
        DATA_DIR /
        nome_arquivo
    )

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
        f"[DOWNLOAD] Salvo: "
        f"{destino}"
    )

    return destino
