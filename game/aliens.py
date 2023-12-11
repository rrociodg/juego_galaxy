import pygame
from pygame.sprite import Sprite    

class Alien(Sprite):
    def __init__(self, a_game):
        super().__init__()
        self.screen = a_game.screen

        imagen_original = pygame.image.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/objetos/ovni.png")
        self.image = pygame.transform.scale(imagen_original, (80, 80))  # Cambia el tamaño de la imagen

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height


        self.x = float(self.rect.x)
        self.juego = a_game

    def update(self):
        self.x += (self.juego.velocidad_alien * self.juego.flota_direccion)
        self.rect.x = self.x

    def chequear_bordes(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        
    