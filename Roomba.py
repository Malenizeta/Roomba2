import pygame
import concurrent.futures
import os
import json

# Configuración de la pantalla
WIDTH, HEIGHT = 1440, 720
COLS, ROWS = 12, 6
CELL_SIZE = WIDTH // COLS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def load_levels():
    with open("niveles.json", "r") as file:
        data = json.load(file)
    return [
        Level(tuple(level["inicio"]), tuple(level["fin"]), level["obstaculos"], "Tile1.jpg")
        for level in data
    ]

class Level:
     # Inicializa el nivel con la posición inicial y final del jugador, obstáculos y la imagen de la celda pintada
    def __init__(self, player_start, player_end, obstacles, painted_cell_image):
        self.player_start = player_start
        self.player_end = player_end
        self.obstacles = obstacles
        self.painted_cell_image = pygame.image.load(os.path.join("Tiles", painted_cell_image))
        self.painted_cell_image = pygame.transform.scale(self.painted_cell_image, (CELL_SIZE, CELL_SIZE))

        try:
            # Inicializa las celdas pintadas y calcula la pintura restante
            self.painted_cells = {player_start}
            self.pintura_restante = self.calcular_pintura()
        except pygame.error as e:
            print(f"Error al cargar la imagen de la celda pintada: {e}")
            self.painted_cell_image = None
    
    #Es un cálculo simple y rápido, por lo que no es necesario usar hilos
    #def calcular_pintura(self):
    #   with concurrent.futures.ThreadPoolExecutor() as executor:
    #       total_celdas = ROWS * COLS
    #       obstaculos_celdas = sum(executor.map(len, [obstacle["cells"] for obstacle in self.obstacles]))
    #        return total_celdas - obstaculos_celdas - len(self.painted_cells)
    
    # Calcula la cantidad de celdas que quedan por pintar
    def calcular_pintura(self):
        total_celdas = ROWS * COLS
        obstaculos_celdas = sum(len(obstacle["cells"]) for obstacle in self.obstacles)
        return total_celdas - obstaculos_celdas - len(self.painted_cells)
    
    # Carga las imágenes de los obstáculos
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
    
    # Procesa cada obstáculo para cargar su imagen y calcular su rectángulo
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

class Game:
    def __init__(self, levels):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font("futuraM.ttf", 36)
        pygame.display.set_caption("Roomba y el Desafío del Papel Pintado")
        self.levels = levels
        self.current_level_index = 0
        self.load_level()

    # Carga el nivel actual
    def load_level(self):
        self.level = self.levels[self.current_level_index]
        self.obstacle_images = self.level.cargar_imagenes_obstaculos()
        self.player_pos = list(self.level.player_start)  
        self.level.painted_cells = {self.level.player_start: 3} 
        self.level.pintura_restante = self.level.calcular_pintura()   
    
    # Dibuja la cuadrícula del nivel
    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (row, col) in self.level.painted_cells:
                    self.screen.blit(self.level.painted_cell_image, rect)
                elif any((row, col) in obstacle["cells"] for obstacle in self.level.obstacles):
                    pygame.draw.rect(self.screen, BLACK, rect)
                elif (row, col) == self.level.player_end:
                    pygame.draw.rect(self.screen, BLACK, rect, 2)  
                    text_surface = self.font.render("FINAL", True, BLACK)
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)
        for img, rect in self.obstacle_images:
            self.screen.blit(img, rect)

    # Reinicia el nivel actual  
    def reset_level(self):
        self.player_pos = list(self.level.player_start)
        self.level.painted_cells = {self.level.player_start: 3}
        self.level.pintura_restante = self.level.calcular_pintura()
        print("Nivel reiniciado")
    
    # Avanza al siguiente nivel o muestra la pantalla de fin de juego
    def next_level(self):
        self.current_level_index += 1
        if self.current_level_index < len(self.levels):
            self.load_level()
        else:
            final_image = pygame.image.load(os.path.join("Tiles", "Final.jpg"))
            final_image = pygame.transform.scale(final_image, (WIDTH, HEIGHT))
            self.screen.blit(final_image, (0, 0))
            text_surface = self.font.render("¡JUEGO COMPLETADO!", True, BLACK)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            exit()

    # Mueve al jugador según la tecla presionada
    def move_player(self, event):
        new_pos = self.player_pos[:]
        if event.key == pygame.K_UP:
            new_pos[0] -= 1
        elif event.key == pygame.K_DOWN:
            new_pos[0] += 1
        elif event.key == pygame.K_LEFT:
            new_pos[1] -= 1
        elif event.key == pygame.K_RIGHT:
            new_pos[1] += 1
        
        if (0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS and tuple(new_pos) not in [cell for obs in self.level.obstacles for cell in obs["cells"]]):
            if tuple(new_pos) in self.level.painted_cells:
                self.reset_level()
            else:
                self.level.pintura_restante -= 1
                self.level.painted_cells[tuple(new_pos)] = 1
                self.player_pos = new_pos
        if self.level.pintura_restante <= 0 and tuple(self.player_pos) == self.level.player_end:
             self.next_level()

    # Bucle principal del juego
    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)
            self.draw_grid()
            pygame.draw.rect(self.screen, BLACK, (self.player_pos[1] * CELL_SIZE, self.player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.move_player(event)
        pygame.quit()
    
  
if __name__ == "__main__":
    levels = load_levels()  
    Game(levels).run()