import pygame

class Nave:
    def __init__(self, a_game):
        self.screen = a_game.screen
        self.screen_rect = a_game.screen.get_rect()

        imagen_original = pygame.image.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/objetos/nave.png")
        self.imagen = pygame.transform.scale(imagen_original, (70, 70))  

        self.rect = self.imagen.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom 
        self.mover_derecha = False
        self.mover_izquierda = False 
        self.velocidad = a_game.velocidad_nave
        

    def mover(self):
        if self.mover_derecha and self.rect.right < self.screen_rect.right:
            self.rect.x += self.velocidad
        if self.mover_izquierda and self.rect.left > 0:
            self.rect.x -= self.velocidad
            

    def corre(self):
        self.screen.blit(self.imagen, self.rect)    

        # # Dibujar un borde alrededor de la nave
        # borde_color = (255, 0, 0)  # Rojo
        # borde_ancho = 2  # Ancho del borde en píxeles
        # pygame.draw.rect(self.screen, borde_color, self.rect, borde_ancho)

    def centrar_nave(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y) 