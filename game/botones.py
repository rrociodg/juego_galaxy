import pygame.font 
from time import sleep

ruta_fuente = "JUEGO_FINAL.py/juego_2.py/recursos_galaxia/gamer.ttf"

class Boton:
    def __init__(self, a_game, imagen, x, y, fuente=ruta_fuente, tamano=35, color=(255, 0, 255), texto_color=(0, 0, 0), transparencia=0):
        self.screen = a_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.color = color
        self.texto_color = texto_color

        # Cargar la imagen y escalar según sea necesario
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen, (self.width, self.height))

        self.rect = self.imagen.get_rect()
        self.rect.x, self.rect.y = x, y
        
        self.transparencia = transparencia

    def prepara_texto(self, texto):
        self.texto_imagen = self.font.render(texto, True, self.texto_color)
        if self.transparencia > 0:
            self.texto_imagen.set_alpha(255 - self.transparencia)  # Aplica la transparencia al fondo del texto
        self.texto_imagen_rect = self.texto_imagen.get_rect()
        self.texto_imagen_rect.center = self.rect.center

    def dibuja_boton(self):
        self.screen.blit(self.imagen, self.rect)