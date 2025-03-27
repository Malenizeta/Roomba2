from django.http import JsonResponse

# Definición simple de la clase Level para representar los niveles.
class Level:
    def __init__(self, player_start, player_end, obstaculos, tile_image):
        self.player_start = player_start
        self.player_end = player_end
        self.obstaculos = obstaculos
        self.tile_image = tile_image

# Función que convierte un objeto Level en un diccionario serializable a JSON.
def serialize_level(level):
    return {
        "inicio": list(level.player_start),  # Convertimos la tupla a lista
        "fin": list(level.player_end),
        "obstaculos": [
            {
                # Convertimos el set de celdas a una lista de listas
                "cells": [list(cell) for cell in obstacle["cells"]],
                "image": obstacle["image"]
            }
            for obstacle in level.obstaculos
        ],
        "tile_image": level.tile_image
    }

# Vista que devuelve los niveles en formato JSON.
def cargar_niveles(request):
    levels = [
        Level(
            (0, 0), (5, 10), 
            [
                {"cells": {(2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5)}, "image": "obstacle1.jpg"},
                {"cells": {(1, 7), (1, 8), (2, 7), (2, 8)}, "image": "obstacle2.jpg"},
                {"cells": {(0, 10), (0, 11), (1, 10), (1, 11), (2, 10), (2, 11)}, "image": "obstacle3.jpg"},
                {"cells": {(3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1)}, "image": "obstacle4.jpg"}
            ], 
            "Tile1.jpg"
        ),

        Level(
            (0, 0), (0, 9), 
            [
                {"cells": {(2, 3), (2, 4), (3, 3), (3, 4), (4, 3), (4, 4), (5, 3), (5, 4)}, "image": "obstacle8.jpg"},
                {"cells": {(2, 9), (2, 10), (3, 9), (3, 10), (4, 9), (4, 10)}, "image": "obstacle9.jpg"},
                {"cells": {(0, 7), (0, 8), (1, 7), (1, 8)}, "image": "obstacle10.jpg"}
            ], 
            "Tile3.jpg"
        ),

        Level(
            (3, 2), (1, 10), 
            [
                {"cells": {(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5)}, "image": "obstacle11.jpg"},
                {"cells": {(3, 7), (3, 8), (3, 9), (3, 10), (4, 7), (4, 8), (4, 9), (4, 10)}, "image": "obstacle12.jpg"}
            ], 
            "Tile4.jpg"
        ),
        
        Level(
            (2, 4), (1, 10), 
            [ 
                {"cells": {(1, 2), (2, 2), (3, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3)}, "image": "obstacle5.jpg"},
                {"cells": {(2, 6), (3, 6)}, "image": "obstacle6.jpg"},
                {"cells": {(3, 9), (3, 10), (4, 9), (4, 10)}, "image": "obstacle7.jpg"}
            ], 
            "Tile2.jpg"
        ),
    ]
    # Serializamos cada nivel y lo devolvemos como JSON.
    data = [serialize_level(level) for level in levels]
    return JsonResponse(data, safe=False)
