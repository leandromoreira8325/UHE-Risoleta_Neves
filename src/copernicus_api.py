"""
copernicus_api.py

Cliente para autenticação no Copernicus Data Space Ecosystem (CDSE).

Projeto:
Monitoramento de Macrófitas Aquáticas
UHE Risoleta Neves

Autor:
Leandro Alves Moreira
"""

from __future__ import annotations

import os
from typing import Optional

import requests


class CopernicusDataSpaceAPI:
    """
    Cliente de autenticação do Copernicus Data Space Ecosystem.

    Variáveis de ambiente necessárias:

    COPERNICUS_CLIENT_ID
    COPERNICUS_CLIENT_SECRET
    """

    TOKEN_URL = (
        "https://identity.dataspace.copernicus.eu/"
        "auth/realms/CDSE/protocol/openid-connect/token"
    )

    def __init__(self) -> None:

        self.client_id = os.getenv(
            "COPERNICUS_CLIENT_ID"
        )

        self.client_secret = os.getenv(
            "COPERNICUS_CLIENT_SECRET"
        )

    def credenciais_configuradas(self) -> bool:
        """
        Verifica se as credenciais foram informadas.
        """

        return bool(
            self.client_id and self.client_secret
        )

    def obter_token(self) -> Optional[str]       Realiza autenticação OAuth2.

        Returns
        -------
        Optional[str]

            Access token válido ou None.
        """

        if not self.credenciais_configuradas():

            print(
                "[COPERNICUS] "
                "Credenciais não encontradas."
            )

            print(
                "[COPERNICUS] "
                "Modo de simulação ativado."
            )

            return None

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        try:

            print(
                "[COPERNICUS] "
                "Solicitando token..."
            )

            response = requests.post(
                self.TOKEN_URL,
                data=payload,
                timeout=30
            )

            response.raise_for_status()

            token = response.json().get(
                "access_token"
            )

            if token:

                print(
                    "[COPERNICUS] "
                    "Token obtido com sucesso."
                )

                return token

            print(
                "[COPERNICUS] "
                "Token não encontrado na resposta."
            )

            return None

        except requests.exceptions.RequestException as exc:

            print(
                "[COPERNICUS ERRO] "
                f"{exc}"
            )

            return None

    def validar_autenticacao(self) -> bool:
        """
        Testa se o token pode ser obtido.
        """

        token = self.obter_token()

        return token is not None


def testar_conexao() -> None:

    cliente = CopernicusDataSpaceAPI()

    if cliente.validar_autenticacao():

        print(
            "[TESTE] "
            "Autenticação realizada com sucesso."
        )

    else:

        print(
            "[TESTE] "
            "Autenticação indisponível."
        )


if __name__ == "__main__":

    testar_conexao()
