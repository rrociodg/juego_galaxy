import pygame

class Estadisticas:
    def __init__(self, a_game):
        self.reinicia()
        self.juego = a_game
        self.reinicia()
        self.nivel = 1

    def reinicia(self):
        self.naves_faltantes = 3