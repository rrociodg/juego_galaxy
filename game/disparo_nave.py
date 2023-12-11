from typing import Any
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, a_game):
        super().__init__()
        self.screen = a_game.screen
        self.color = a_game.colorbala
        self.rect = pygame.Rect(0,0, a_game.anchobala, a_game.altobala)
        self.rect.midtop = a_game.nave.rect.midtop
        self.juego = a_game
        self.y = float(self.rect.y)
        self.bullets_allowed = 3
        self.aliens_puntaje = 50

        imagen_original = pygame.image.load('JUEGO_FINAL.py/juego_2.py/recursos_galaxia/objetos/disparonave.png')  # Carga la imagen
        self.imagen = pygame.transform.scale(imagen_original, (20, 20))  

        self.rect = self.imagen.get_rect()  # Obtiene el rectángulo que encierra la imagen
        self.rect.midtop = a_game.nave.rect.midtop


        self.sonido = pygame.mixer.Sound("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/laser2.mp3")
        self.sonido.play()
    
    def update(self):
        self.y -= self.juego.velocidad
        self.rect.y = self.y
        self.bullets = self.juego.bullets
        self.aliens = self.juego.aliens


        self.choques = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True) #primer grupo es el de las balas y el segundo el de los aliens

        if self.choques:
            for aliens in self.choques.values():
                self.juego.score += self.aliens_puntaje * len(aliens)
                self.juego.tablaP.prep_score()
                self.juego.tablaP.check_high_score()


    def draw_bullet(self):
        self.screen.blit(self.imagen, self.rect)