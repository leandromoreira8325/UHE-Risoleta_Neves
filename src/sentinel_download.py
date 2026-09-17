"""
sentinel_download.py
"""

from pathlib import Path

import requests

from src.config import DATA_DIR
from src.copernicus_api import CopernicusDataSpaceAPI


def baixar_produto(
    product_id: str,
    nome_produto: str
):

    api = CopernicusDataSpaceAPI()

    token = api.obter_token()

    print(
        f"[DOWNLOAD] Product ID: "
        f"{product_id}"
    )

    print(
        f"[DOWNLOAD] Produto: "
        f"{nome_produto}"
    )

    destino = (
        DATA_DIR /
        f"{nome_produto}.zip"
    )

    url = (
        "https://download.dataspace.copernicus.eu/"
        f"odata/v1/Products({product_id})/$value"
    )

    print(
        f"[DOWNLOAD] URL:"
    )

    print(url)

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            stream=True,
            timeout=300
        )

        print(
            f"[DOWNLOAD] Status:"
            f" {response.status_code}"
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
            f"[DOWNLOAD] Arquivo salvo:"
        )

        print(destino)

        return destino

    except Exception as erro:

        print(
            "[DOWNLOAD ERRO]"
        )

        print(erro)

        raise
