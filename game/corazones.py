import pygame
from pygame.sprite import Sprite
import random

class Corazones(Sprite):
    def __init__(self, a_game):
        super().__init__()
        self.screen = a_game.screen
        self.screen_rect = a_game.screen.get_rect()
        self.velocidad = 0.5

        self.image = pygame.image.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/icono/corazonicono.png")
        self.rect = self.image.get_rect()

        escala = 0.10  # Puedes ajustar este valor según tus necesidades
        new_width = int(self.image.get_width() * escala)
        new_height = int(self.image.get_height() * escala)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, self.screen_rect.width)
        self.rect.y = 0  # parte superior de la pantalla
    
    def update(self):
        self.rect.y += self.velocidad