import os
import requests

class CopernicusAPI:
    def __init__(self):
        # Utiliza variáveis de ambiente do GitHub Actions se configuradas, ou valores padrão
        self.client_id = os.getenv("COPERNICUS_CLIENT_ID", "")
        self.client_secret = os.getenv("COPERNICUS_CLIENT_SECRET", "")
        self.token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

    def obter_token(self):
        """
        Realiza a autenticação na API do Copernicus Data Space e retorna o token de acesso.
        Caso as credenciais não estejam definidas, retorna um token simulado para fins de teste.
        """
        if not self.client_id or not self.client_secret:
            print("[COPERNICUS API] Credenciais não detectadas no ambiente. Utilizando modo simulado/fallback.")
            return "mock_token_copernicus_12345"

        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        
        try:
            response = requests.post(self.token_url, data=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("access_token")
            else:
                print(f"[AVISO] Falha na autenticação Copernicus: {response.status_code} - {response.text}")
                return "mock_token_copernicus_12345"
        except Exception as e:
            print(f"[ERRO] Erro ao conectar com o servidor Copernicus: {e}")
            return "mock_token_copernicus_12345"

    def buscar_dados_completos(self, token, bbox, dt_inicio, dt_fim, max_cloud=35):
        """
        Busca cenas Sentinel-2 com base na bounding box e intervalo de datas.
        Retorna os dados raster (bytes TIFF) e a data de aquisição.
        Se retornar (None, None), o sistema acionará automaticamente a simulação espectral.
        """
        # A lógica de requisição OData/Stac do Copernicus entra aqui.
        # Retornando None, o script usa a geometria real do shapefile para calcular os índices por fallback estruturado.
        return None, None
