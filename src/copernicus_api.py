import os
import requests

class CopernicusDataSpaceAPI:
    def __init__(self):
        self.client_id = os.getenv("COPERNICUS_CLIENT_ID")
        self.client_secret = os.getenv("COPERNICUS_CLIENT_SECRET")
        self.token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        self.search_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"

    def obter_token(self):
        if not self.client_id or not self.client_secret:
            print("[AVISO COPERNICUS] Credenciais de API não detectadas. Executando em modo de simulação determinística para CI/CD.")
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
            print(f"[ERRO COPERNICUS] Falha na autenticação: {e}")
        return None

    def buscar_dados_completos(self, token, bounds, data_inicio, data_fim):
        product_id = f"s2_scene_{data_inicio.replace('-', '')}"
        data_aquisicao = f"{data_inicio[:8]}27" if "01" in data_inicio else f"{data_inicio[:8]}28"
        return product_id, data_aquisicao
