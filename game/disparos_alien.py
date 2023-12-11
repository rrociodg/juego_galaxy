from pygame.sprite import Sprite
import pygame

class AlienBullet(Sprite):
    def __init__(self, a_game, alien):
        super().__init__()
        self.screen = a_game.screen
        self.color = a_game.colorbalaalien
        self.juego = a_game
        self.rect = pygame.Rect(0, 0, a_game.anchobalaalien, a_game.altobalaalien)

        imagen_original = pygame.image.load('JUEGO_FINAL.py/juego_2.py/recursos_galaxia/objetos/balasaliens.png')  # Carga la imagen
        self.imagen = pygame.transform.scale(imagen_original, (20, 50))  

        self.rect = self.imagen.get_rect()
        self.rect.midbottom = alien.rect.midbottom

        self.y = float(self.rect.y)

    def update(self):
        self.y += self.juego.velocidad_alien
        self.rect.y = self.y

        # Verifica si la bala ha alcanzado la parte inferior de la pantalla
        if self.rect.bottom >= self.juego.alto:
            self.kill()  # Elimina la bala si llega al final de la pantalla

    def draw_bullet(self):
        self.screen.blit(self.imagen, self.rect)