import random
import pygame
from pygame.sprite import Sprite

class Moneda(Sprite):
    def __init__(self, a_game):
        super().__init__()
        self.screen = a_game.screen
        self.screen_rect = a_game.screen.get_rect()
        self.velocidad = 0.5  # Ajusta la velocidad de caída de las monedas según sea necesario

        imagen_moneda = pygame.image.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/objetos/moneda.png")  # Asegúrate de proporcionar la ruta correcta a la imagen de la moneda
        self.image = pygame.transform.scale(imagen_moneda, (imagen_moneda.get_width() // 30, imagen_moneda.get_height() // 30))

        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(0, self.screen_rect.width)
        self.rect.y = 0  # parte superior de la pantalla

        
    def update(self):
        self.rect.y += self.velocidad

