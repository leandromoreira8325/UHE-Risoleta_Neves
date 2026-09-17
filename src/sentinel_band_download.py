"""
sentinel_band_download.py
"""

import requests

from src.copernicus_api import (
    CopernicusDataSpaceAPI
)


def testar_download(url: str):

    api = CopernicusDataSpaceAPI()

    token = api.obter_token()

    print("\nTOKEN (30 primeiros):")
    print(token[:30])

    headers = {
        "Authorization": f"Bearer {token}"
    }

    resposta = requests.get(
        url,
        headers=headers,
        allow_redirects=False,
        timeout=120
    )

    print("\nSTATUS:")
    print(resposta.status_code)

    print("\nHEADERS:")
    print(dict(resposta.headers))

    print("\nTEXTO:")
    print(resposta.text[:500])
