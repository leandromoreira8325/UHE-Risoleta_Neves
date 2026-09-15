"""
sentinel_search.py

Busca de cenas Sentinel-2 utilizando
o catálogo STAC do Copernicus Data Space.

Projeto:
Monitoramento de Macrófitas
UHE Risoleta Neves
"""

from pystac_client import Client

CATALOGO_STAC = (
    "https://catalogue.dataspace.copernicus.eu/stac"
)


def listar_colecoes():

    catalog = Client.open(CATALOGO_STAC)

    print("\nCOLEÇÕES DISPONÍVEIS\n")

    for collection in catalog.get_collections():

        print(
            collection.id
        )


if __name__ == "__main__":

    listar_colecoes()
