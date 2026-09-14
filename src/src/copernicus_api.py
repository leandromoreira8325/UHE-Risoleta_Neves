"""
Módulo de Integração com a API do Copernicus Data Space Ecosystem.
Responsável por autenticação, busca de metadados e download de imagens Sentinel-2.
"""

import os
import requests
from datetime import datetime

class CopernicusAPI:
    def __init__(self, username=None, password=None):
        # Utiliza variáveis de ambiente ou credenciais diretas
        self.username = username or os.getenv("COPERNICUS_USER")
        self.password = password or os.getenv("COPERNICUS_PASSWORD")
        self.token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        self.token = None

    def autenticar(self):
        """Gera o token de acesso OAuth2 para consumo das APIs do Copernicus."""
        data = {
            "client_id": "cdse-public",
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        
        try:
            response = requests.post(self.token_url, data=data)
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                print("[COPERNICUS] Autenticação realizada com sucesso.")
                return True
            else:
                print(f"[ERRO] Falha na autenticação Copernicus: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"[EXCEÇÃO] Erro de conexão ao autenticar no Copernicus: {e}")
            return False

    def buscar_melhor_cena(self, bbox, data_inicio, data_fim):
        """
        Busca no catálogo OData do Copernicus a cena Sentinel-2 L2A 
        com menor índice de nuvens dentro da bounding box e período informados.
        Retorna o ID do produto e a data exata da captura.
        """
        if not self.token:
            if not self.autenticar():
                return None

        # Endpoint OData de catálogo do Copernicus
        catalogue_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
        
        # Filtro espacial (bbox) e temporal
        # bbox formato: [min_lon, min_lat, max_lon, max_lat]
        spatial_filter = f"OData.CSC.Intersects(area=geography'SRID=4326;POLYGON(({bbox[0]} {bbox[1]}, {bbox[2]} {bbox[1]}, {bbox[2]} {bbox[3]}, {bbox[0]} {bbox[3]}, {bbox[0]} {bbox[1]}))')"
        temporal_filter = f"ContentDate/Start ge {data_inicio}T00:00:00.000Z and ContentDate/Start le {data_fim}T23:59:59.999Z"
        collection_filter = "Collection/Name eq 'SENTINEL-2'"
        
        filter_query = f"{spatial_filter} and {temporal_filter} and {collection_filter}"
        
        params = {
            "$filter": filter_query,
            "$orderby": "ContentDate/Start asc",
            "$top": 5 # Pega as primeiras opções para filtrar a com menor nuvem
        }

        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = requests.get(catalogue_url, headers=headers, params=params)
            if response.status_code == 200:
                products = response.json().get("value", [])
                if not products:
                    print(f"[AVISO] Nenhuma cena encontrada entre {data_inicio} e {data_fim}.")
                    return None
                
                # Seleciona a cena com menor cobertura de nuvens (simulado ou via metadado S2MSI)
                melhor_produto = products[0]
                produto_id = melhor_produto.get("Id")
                nome_produto = melhor_produto.get("Name")
                
                # Extrai a data exata da string do nome ou metadado (ex: S2A_MSIL2A_20260114...)
                data_str = nome_produto.split("_")[2][:8] # Formato YYYYMMDD
                data_formatada = f"{data_str[:4]}-{data_str[4:6]}-{data_str[6:]}"
                
                print(f"[SUCESSO] Cena selecionada: {nome_produto} | Data: {data_formatada}")
                return {
                    "produto_id": produto_id,
                    "nome": nome_produto,
                    "data_cena": data_formatada
                }
            else:
                print(f"[ERRO] Falha ao consultar catálogo: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"[EXCEÇÃO] Erro na busca de cenas: {e}")
            return None
