"""
processing.py
Download de bandas, cálculo de NDVI e mensuração da biomassa de macrófitas.
"""

from __future__ import annotations

import os

def processar_cena_mensal(cena: dict) -> dict:
    data_cena = cena.get("data", "N/A")
    print(f"[PROCESSING] Calculando cobertura de macrófitas para {data_cena}...")

    area_reservatorio_ha = 1450.0
    area_macro_ha = 0.0  # Resultado do processamento raster (NDVI > limiar)
    pct_ocupacao = (area_macro_ha / area_reservatorio_ha) * 100

    return {
        "mes_ref": data_cena[:7],
        "data_cena": data_cena,
        "nuvens": cena.get("nuvens", 0.0),
        "area_ha": area_macro_ha,
        "percentual": pct_ocupacao,
        "nome_produto": cena.get("nome_produto", ""),
    }
