class CopernicusAPI:
    def __init__(self):
        pass
    
    def buscar_cenas_recentes(self):
        print("Buscando metadados de cenas Sentinel-2...")
        # Retorna dados estruturados para o pipeline
        return [{"data": "2026-06-01", "nuvens": 1.2, "id": "S2_ID_EXEMPLO"}]
