from src.config import OUTPUT_DIR
from src.processing import processar_dados_2026
from src.mapping import gerar_mapa_macrophitas
from src.report import gerar_relatorio_pdf


def main():

    print(
        "=== UHE Risoleta Neves ==="
    )

    dados_serie, shp = processar_dados_2026()

    ultimo = dados_serie[-1]

    mapa = gerar_mapa_macrophitas(
        shp,
        ultimo,
        OUTPUT_DIR
    )

    gerar_relatorio_pdf(
        dados_serie,
        mapa,
        OUTPUT_DIR
    )

    print(
        "=== Pipeline finalizado ==="
    )


if __name__ == "__main__":
    main()
