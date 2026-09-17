from __future__ import annotations

import os
import requests


class CopernicusDataSpaceAPI:

    TOKEN_URL = (
        "https://identity.dataspace.copernicus.eu/"
        "auth/realms/CDSE/protocol/openid-connect/token"
    )

    def __init__(self):

        self.client_id = os.getenv(
            "COPERNICUS_CLIENT_ID"
        )

        self.client_secret = os.getenv(
            "COPERNICUS_CLIENT_SECRET"
        )

    def obter_token(self):

        if (
            not self.client_id
            or
            not self.client_secret
        ):

            raise RuntimeError(
                "Credenciais não encontradas."
            )

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        response = requests.post(
            self.TOKEN_URL,
            data=payload,
            timeout=60
        )

        response.raise_for_status()

        token = response.json().get(
            "access_token"
        )

        if token is None:

            raise RuntimeError(
                "Token não retornado."
            )

        return token


if __name__ == "__main__":

    api = CopernicusDataSpaceAPI()

    token = api.obter_token()

    print(
        f"TOKEN OK: {token[:30]}..."
    )
