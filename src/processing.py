from src.config import SHAPEFILE_PATH
from src.sentinel_search import buscar_melhor_cena


def processar_dados_2026():

    print(
        "[PROCESSING] Iniciando..."
    )

    cena = buscar_melhor_cena()

    if cena is None:

        raise RuntimeError(
            "Nenhuma cena Sentinel encontrada."
        )

    dados_serie = [

        {
            "mes": str(
                cena["data"]
            )[:7],

            "area_ha": 0.0,

            "percentual": 0.0,

            "status":
                f"Sentinel-2 ({cena['nuvens']} % nuvem)"
        }
    ]

    return (
        dados_serie,
        str(SHAPEFILE_PATH)
    )
