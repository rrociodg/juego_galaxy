import pygame
import time

class Cronometro:
    def __init__(self, game):
        self.inicio_tiempo = 0
        self.tiempo_transcurrido = 0
        self.cronometro_activo = False
        self.font = pygame.font.Font(None, 36)
        self.game = game

    def iniciar_cronometro(self):
        if self.inicio_tiempo is None:
            self.inicio_tiempo = pygame.time.get_ticks()

    def detener_cronometro(self):
        self.inicio_tiempo = None

    def reiniciar_cronometro(self):
        self.inicio_tiempo = time.time()
        self.tiempo_transcurrido = 0
        self.cronometro_activo = False

    def obtener_tiempo_transcurrido(self):
        if self.inicio_tiempo is not None:
            return (pygame.time.get_ticks() - self.inicio_tiempo) / 1000  # Dividir por 1000 para convertir milisegundos a segundos
        return 0
    
    def mostrar_cronometro(self): 
        tiempo = self.obtener_tiempo_transcurrido() 
        texto = self.font.render(f'{tiempo} ', True, (255, 255, 255)) 
        self.game.screen.blit(texto, (12, 10))  # Usa la referencia del juego para acceder a la pantalla