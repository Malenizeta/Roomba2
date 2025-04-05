import pygame
import os
from cliente.level import Level
from cliente.const import WIDTH, HEIGHT, CELL_SIZE, BLACK, WHITE, ROWS, COLS


class Game:
    def __init__(self, levels):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font("futuraM.ttf", 36)
        pygame.display.set_caption("Roomba y el Desafío del Papel Pintado")
        self.levels = levels
        self.current_level_index = 0
        self.load_level()

    def load_level(self):
        self.level = self.levels[self.current_level_index]
        self.obstacle_images = self.level.cargar_imagenes_obstaculos()
        self.player_pos = list(self.level.player_start)
        self.level.painted_cells = {self.level.player_start: 3}
        self.level.pintura_restante = self.level.calcular_pintura()
        self.obstacle_cells = {
            tuple(cell)
            for obstacle in self.level.obstacles
            for cell in obstacle["cells"]
        }

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
        
        if (0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS and tuple(new_pos) not in self.obstacle_cells):
            if tuple(new_pos) in self.level.painted_cells:
                self.reset_level()
            else:
                self.level.pintura_restante -= 1
                self.level.painted_cells[tuple(new_pos)] = 1
                self.player_pos = new_pos
        if self.level.pintura_restante <= 0 and tuple(self.player_pos) == self.level.player_end:
             self.next_level()

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

