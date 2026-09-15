name: Monitoramento UHE Risoleta Neves

on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout do Repositório
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: Instalar Dependências
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then 
            pip install -r requirements.txt; 
          else 
            pip install geopandas matplotlib shapely reportlab numpy requests rasterio; 
          fi

      - name: Garantir Diretório de Saída
        run: mkdir -p outputs

      - name: Executar Pipeline Principal
        env:
          PYTHONPATH: src
        run: python main.py

      - name: Salvar Artefatos do Relatório
        uses: actions/upload-artifact@v4
        with:
          name: relatorio-e-mapa
          path: outputs/
          if-no-files-found: warn
