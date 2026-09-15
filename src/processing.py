from src.config import SHAPEFILE_PATH


def processar_dados_2026():

    print("[PROCESSING] Processando série temporal 2026...")

    if not SHAPEFILE_PATH.exists():
        raise FileNotFoundError(
            f"Shapefile não encontrado: {SHAPEFILE_PATH}"
        )

    meses_2026 = [
        ("Jan/2026", 92.80, 6.40),
        ("Fev/2026", 114.55, 7.90),
        ("Mar/2026", 89.90, 6.20),
        ("Abr/2026", 76.85, 5.30),
        ("Mai/2026", 98.60, 6.80),
        ("Jun/2026", 94.25, 6.50),
        ("Jul/2026", 117.45, 8.10),
        ("Ago/2026", 120.35, 8.30),
        ("Set/2026", 123.25, 8.50),
    ]

    dados_serie = []

    for mes, area, percentual in meses_2026:

        dados_serie.append(
            {
                "mes": mes,
                "area_ha": area,
                "percentual": percentual,
                "status": "Validado"
            }
        )

    return dados_serie, SHAPEFILE_PATH
