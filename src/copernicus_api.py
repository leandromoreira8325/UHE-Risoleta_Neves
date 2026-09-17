from __future__ import annotations
import os
import requests

class CopernicusDataSpaceAPI:
    TOKEN_URL = (
        "https://identity.dataspace.copernicus.eu/"
        "auth/realms/CDSE/protocol/openid-connect/token"
    )

    def __init__(self):
        self.username = os.getenv("COPERNICUS_USER") or os.getenv("COPERNICUS_USERNAME")
        self.password = os.getenv("COPERNICUS_PASSWORD")
        self.client_id = os.getenv("COPERNICUS_CLIENT_ID")
        self.client_secret = os.getenv("COPERNICUS_CLIENT_SECRET")

    def obter_token(self) -> str:
        if self.username and self.password:
            payload = {
                "grant_type": "password",
                "username": self.username,
                "password": self.password,
                "client_id": "cdse-public"
            }
        elif self.client_id and self.client_secret:
            payload = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        else:
            raise RuntimeError(
                "Credenciais Copernicus não encontradas. "
                "Defina COPERNICUS_USER e COPERNICUS_PASSWORD no GitHub Secrets."
            )

        response = requests.post(self.TOKEN_URL, data=payload, timeout=60)
        response.raise_for_status()

        token = response.json().get("access_token")
        if token is None:
            raise RuntimeError("Token não retornado pela API do Copernicus.")

        return token
