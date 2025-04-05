import pygame
import os
import concurrent.futures
from cliente.const import CELL_SIZE, ROWS, COLS

class Level:
    def __init__(self, player_start, player_end, obstacles, painted_cell_image):
        self.player_start = player_start
        self.player_end = player_end
        self.obstacles = obstacles
        self.painted_cell_image = pygame.image.load(os.path.join("Tiles", painted_cell_image))
        self.painted_cell_image = pygame.transform.scale(self.painted_cell_image, (CELL_SIZE, CELL_SIZE))
        self.painted_cells = {player_start}
        self.pintura_restante = self.calcular_pintura()

    def calcular_pintura(self):
        total_celdas = ROWS * COLS
        obstaculos_celdas = sum(len(obstacle["cells"]) for obstacle in self.obstacles)
        return total_celdas - obstaculos_celdas - len(self.painted_cells)

    def cargar_imagenes_obstaculos(self):
        obstacle_images = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_obstacle = {
                executor.submit(self.procesar_obstaculo, obstacle): obstacle for obstacle in self.obstacles
            }
            for future in concurrent.futures.as_completed(future_to_obstacle):
                result = future.result()
                if result:
                    obstacle_images.append(result)
        return obstacle_images

    def procesar_obstaculo(self, obstacle):
        obstacle_cells = list(obstacle["cells"])
        min_row, max_row = min(c[0] for c in obstacle_cells), max(c[0] for c in obstacle_cells)
        min_col, max_col = min(c[1] for c in obstacle_cells), max(c[1] for c in obstacle_cells)
        obstacle_rect = pygame.Rect(min_col * CELL_SIZE, min_row * CELL_SIZE, (max_col - min_col + 1) * CELL_SIZE, (max_row - min_row + 1) * CELL_SIZE)

        try:
            image_path = os.path.join("Tiles", obstacle["image"])
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (obstacle_rect.width, obstacle_rect.height))
        except pygame.error as e:
            print(f"Error al cargar la imagen del obstáculo {obstacle['image']}: {e}")
            image = None
        return (image, obstacle_rect)