"""
copernicus_api.py

Módulo de autenticação para o Copernicus Data Space Ecosystem (CDSE).

Autor: Leandro Alves Moreira
Projeto: UHE Risoleta Neves - Monitoramento de Macrófitas
"""

from __future__ import annotations

import os
from typing import Optional

import requests


class CopernicusDataSpaceAPI:
    """
    Cliente básico de autenticação do Copernicus Data Space Ecosystem.

    Variáveis de ambiente esperadas:

    COPERNICUS_CLIENT_ID
    COPERNICUS_CLIENT_SECRET
    """

    TOKEN_URL = (
        "https://identity.dataspace.copernicus.eu/"
        "auth/realms/CDSE/protocol/openid-connect/token"
    )

    def __init__(self) -> None:
        self.client_id = os.getenv("COPERNICUS_CLIENT_ID")
        self.client_secret = os.getenv("COPERNICUS_CLIENT_SECRET")

    def obter_token(self) -> Optional[str]:
        """
        Obtém token OAuth2 do Copernicus.

        Returns
        -------
        Optional[str]
            Token de acesso ou None em caso de falha.
        """

        if not self.client_id or not self.client_secret:

            print(
                "[denciais não configuradas. "
                "Modo de simulação ativado."
            )

            return None

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        try:

            response = requests.post(
                self.TOKEN_URL,
                data=payload,
                timeout=30
            )

            response.raise_for_status()

            token = response.json().get("access_token")

            if token:

                print(
                    "[COPERNICUS] Token obtido com sucesso."
                )

                return token

            print(
                "[COPERNICUS] Resposta recebida sem access_token."
            )

            return None

        except requests.exceptions.RequestException as exc:

            print(
                f"[COPERNICUS ERRO] Falha na autenticação: {exc}"
            )

            return None

    def validar_conexao(self) -> bool:
        """
        Verifica se as credenciais são válidas.

        Returns
        -------
        bool
            True se a autenticação foi bem-sucedida.
        """

        token = self.obter_token()

        return token is not None


if __name__ == "__main__":

    api = CopernicusDataSpaceAPI()

    if api.validar_conexao():

        print(
            "[TESTE] Conexão com Copernicus realizada com sucesso."
        )

    else:

        print(
            "[TESTE] Não foi possível autenticar no Copernicus."
        )
