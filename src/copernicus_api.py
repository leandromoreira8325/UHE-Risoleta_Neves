import os
import requests

class CopernicusDataSpaceAPI:
    def __init__(self):
        self.client_id = os.getenv("COPERNICUS_CLIENT_ID")
        self.client_secret = os.getenv("COPERNICUS_CLIENT_SECRET")
        self.token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

    def obter_token(self):
        if not self.client_id or not self.client_secret:
            print("[COPERNICUS] Modo de simulação determinística ativado para CI/CD.")
            return None
        
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        try:
            response = requests.post(self.token_url, data=data, timeout=30)
            if response.status_code == 200:
                return response.json().get("access_token")
        except Exception as e:
            print(f"[COPERNICUS ERRO] Falha na autenticação: {e}")
        return None
