"""
main.py
Execução orquestrada do monitoramento mensal Jan-Set 2026.
"""

from __future__ import annotations

import os
import calendar
from src.sentinel_search import buscar_melhor_cena
from src.processing import processar_cena_mensal
from src.mapping import gerar_mapa_macrophitas
from src.report import gerar_relatorio_consolidado


def executar_pipeline_mensal():
    ano = 2026
    meses = range(1, 10)  # Janeiro (1) a Setembro (9)
    resultados_serie = []
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    print(f"=== Monitoramento Mensal UHE Risoleta Neves ({ano}) ===")

    for mes in meses:
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        data_ini = f"{ano}-{mes:02d}-01"
        data_fim = f"{ano}-{mes:02d}-{ultimo_dia:02d}"

        print(f"\n[PROCESSANDO] Mês {mes:02d}/{ano} ({data_ini} a {data_fim})")

        cena = buscar_melhor_cena(data_ini, data_fim)
        if not cena:
            continue

        dados_mes = processar_cena_mensal(cena)

        sufixo_mes = f"{ano}_{mes:02d}"
        mapa_path = gerar_mapa_macrophitas(
            shapefile_path=None,
            ultimo_dado=dados_mes,
            output_dir=output_dir,
            sufixo=sufixo_mes,
        )

        dados_mes["mapa_path"] = mapa_path
        resultados_serie.append(dados_mes)

    if resultados_serie:
        pdf_path = gerar_relatorio_consolidado(resultados_serie, output_dir)
        print(f"\n=== Sucesso! Relatório consolidado gerado: {pdf_path} ===")
    else:
        print("\n[AVISO] Nenhuma cena foi processada na janela de datas.")


if __name__ == "__main__":
    executar_pipeline_mensal()
