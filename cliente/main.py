from cliente.auth import menu_autenticacion
from cliente.utils import load_levels
from cliente.game import Game

if __name__ == "__main__":
    usuario = menu_autenticacion()
    levels = load_levels()
    if levels:
        Game(levels).run()
    else:
        print("No se pudieron cargar los niveles. Verifique la conexión al servidor.")