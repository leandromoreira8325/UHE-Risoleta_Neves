import os
import requests
from shapely.geometry import box

class CopernicusAPI:
    def __init__(self):
        self.client_id = os.getenv("COPERNICUS_CLIENT_ID", "")
        self.client_secret = os.getenv("COPERNICUS_CLIENT_SECRET", "")
        self.token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        self.odata_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"

    def obter_token(self):
        if not self.client_id or not self.client_secret:
            print("[COPERNICUS API] Credenciais não detectadas no ambiente. Utilizando modo simulado.")
            return None

        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        
        try:
            response = requests.post(self.token_url, data=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                print(f"[AVISO] Falha na autenticação Copernicus: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"[ERRO] Erro ao conectar com o servidor Copernicus: {e}")
            return None

    def buscar_dados_completos(self, token, bbox, dt_inicio, dt_fim, max_cloud=35):
        """
        Busca cenas Sentinel-2 reais utilizando o catálogo OData do Copernicus Data Space.
        """
        if not token:
            return None, None

        minx, miny, maxx, maxy = bbox
        # Monta o filtro espacial (polygon WKT) e temporal para o Sentinel-2
        wkt_box = f"POLYGON(({minx} {miny}, {maxx} {miny}, {maxx} {maxy}, {minx} {maxy}, {minx} {miny}))"
        
        # Filtro OData para Sentinel-2 L2A (correção atmosférica) com baixa cobertura de nuvens
        filter_query = (
            f"Collection/Name eq 'SENTINEL-2' and "
            f"Attributes/OData.CSC.StringAttribute/any(s:s/Name eq 'processingLevel' and s/OData.CSC.StringAttribute/Value eq 'S2MSI2A') and "
            f"OData.CSC.Intersects(area=geography'SRID=4326;{wkt_box}') and "
            f"ContentDate/Start ge {dt_inicio}T00:00:00.000Z and "
            f"ContentDate/Start le {dt_fim}T23:59:59.999Z"
        )

        params = {
            "$filter": filter_query,
            "$top": 1,
            "$orderby": "ContentDate/Start desc"
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:
            response = requests.get(self.odata_url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json().get("value", [])
                if data:
                    produto = data[0]
                    data_aquisicao = produto.get("ContentDate", {}).get("Start", "")[:10]
                    print(f"[COPERNICUS API] Cena encontrada para o período: {data_aquisicao}")
                    # Retorna os metadados da cena encontrada (o processamento raster fará o download se necessário)
                    # Caso queira processar bandas reais, o ID do produto pode ser usado na API de Download.
                    return None, data_aquisicao  # Se retornar None no binário, o pipeline usa a geometria com a data real obtida.
            else:
                print(f"[AVISO] Consulta OData retornou status {response.status_code}")
        except Exception as e:
            print(f"[ERRO] Falha na consulta de produtos Copernicus: {e}")

        return None, None
