"""
sentinel_band_download.py

Download direto das bandas Sentinel-2
a partir dos links retornados pelo STAC.
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
        "Authorization": (
            f"Bearer {token}"
        )
    }

    print(
        f"[DOWNLOAD] {nome_arquivo}"
    )

    resposta = requests.get(
        url,
        headers=headers,
        stream=True,
        timeout=300,
        allow_redirects=True
    )

    print(
        f"[DOWNLOAD] Status: "
        f"{resposta.status_code}"
    )

    print(
        "[DOWNLOAD] Headers:"
    )

    print(
        dict(
            resposta.headers
        )
    )

    if resposta.status_code != 200:

        print(
            "[DOWNLOAD] Corpo da resposta:"
        )

        print(
            resposta.text[:1000]
        )

        resposta.raise_for_status()

    with open(
        destino,
        "wb"
    ) as arquivo:

        for chunk in (
            resposta.iter_content(
                chunk_size=8192
            )
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
):

    arquivos = {}

    arquivos["B03"] = (
        baixar_banda(
            cena["B03"],
            "B03_10m.jp2"
        )
    )

    return arquivos
