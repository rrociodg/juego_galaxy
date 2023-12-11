import random
import pygame
from pygame.sprite import Sprite

class Asteroide(Sprite):
    def __init__(self, a_game):
        super().__init__()
        self.screen = a_game.screen
        self.screen_rect = a_game.screen.get_rect()
        self.velocidad = 0.5
        self.velocidad_x = random.uniform(-1, 1)

        imagen_original = pygame.image.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/objetos/asteroide.png")
        self.image = pygame.transform.scale(imagen_original, (imagen_original.get_width() // 10, imagen_original.get_height() // 10))

        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(0, self.screen_rect.width)
        self.rect.y = 0

    def update(self):
        self.rect.y += self.velocidad
        self.rect.x += self.velocidad_x 

    def draw(self):
        # Dibujar el asteroide
        self.screen.blit(self.image, self.rect)

        # Dibujar un borde alrededor del asteroide
        borde_color = (255, 0, 0)  # Rojo
        borde_ancho = 2  # Ancho del borde en píxeles
        pygame.draw.rect(self.screen, borde_color, self.rect, borde_ancho)