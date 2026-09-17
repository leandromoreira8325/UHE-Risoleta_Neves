"""
sentinel_download.py

Download de produtos Sentinel-2.
"""

from pathlib import Path

import requests

from src.config import DATA_DIR
from src.copernicus_api import CopernicusDataSpaceAPI


def baixar_produto(
    product_id: str,
    nome_produto: str
) -> Path:

    api = CopernicusDataSpaceAPI()

    token = api.obter_token()

    destino = (
        DATA_DIR /
        f"{nome_produto}.zip"
    )

    url = (
        "https://download.dataspace.copernicus.eu/"
        f"odata/v1/Products({product_id})/$value"
    )

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    print(
        f"[DOWNLOAD] Iniciando download: "
        f"{nome_produto}"
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

                arquivo.write(chunk)

    print(
        f"[DOWNLOAD] Arquivo salvo:"
    )

    print(destino)

    return destino


if __name__ == "__main__":

    print(
        "Módulo Sentinel Download carregado."
    )
