import requests
from cliente.const import WIDTH, HEIGHT, CELL_SIZE, COLS, ROWS, BLACK, WHITE

def load_levels():
    from cliente.level import Level
    try:
        response = requests.get("http://127.0.0.1:8000/api/levels/")
        response.raise_for_status()
        data = response.json()
        print(f"Se han cargado {len(data)} niveles desde el servidor.")
        return [
            Level(tuple(level["inicio"]), tuple(level["fin"]), level["obstaculos"], level["tile_image"])
            for level in data
        ]
    except requests.RequestException as e:
        print(f"Error al cargar los niveles desde el servidor: {e}")
        return []