import pygame.font
from pygame.sprite import Group #cantidad de corazones que van a contener el mismo tipo de codigo 
from corazones import Corazones
import sqlite3

class TablaPuntajes:
    def __init__(self, a_game):
        self.screen = a_game.screen 
        self.screen_rect = self.screen.get_rect()
        self.juego = a_game
        self.estadisticas = a_game.estadisticas
        self.conn = sqlite3.connect('jugadores.db')

        self.color_texto = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_corazones()

    def prep_score(self):
        self.score_str = str(self.juego.score)
        self.score_imagen = self.font.render(self.score_str, True, self.color_texto, None)

        self.score_rect = self.score_imagen.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        # Obtener el puntaje más alto desde la base de datos
        self.juego.high_score = self.obtener_puntaje_mas_alto()
        self.highscore_str = str(self.juego.high_score)
        self.highscore_imagen = self.font.render(self.highscore_str, True, self.color_texto, None)

        self.highscore_rect = self.highscore_imagen.get_rect()
        self.highscore_rect.centerx = self.screen_rect.centerx
        self.highscore_rect.top = self.score_rect.top

    def guardar_puntaje(self, nombre, puntaje):
        try:
            print(f"Guardando puntaje: Nombre={nombre}, Puntaje={puntaje}")
            sql = 'INSERT INTO jugadores (nombre, puntaje) VALUES (?, ?)'
            self.conn.execute(sql, (nombre, puntaje))
            self.conn.commit()
            print(f"Puntaje guardado correctamente. Filas afectadas: {self.conn.total_changes}")
        except Exception as e:
            print(f"Error al guardar puntaje: {e}")
    
    def obtener_puntaje_mas_alto(self):
        # Obtener el puntaje más alto desde la base de datos
        cursor = self.conn.execute('''
        SELECT MAX(puntaje) FROM jugadores
        ''')
        max_puntaje = cursor.fetchone()[0]
        return max_puntaje

    def obtener_top_jugadores(self):
        # Obtener el top 5 de jugadores desde la base de datos
        cursor = self.conn.execute('''
        SELECT nombre, puntaje
        FROM jugadores
        ORDER BY puntaje DESC
        LIMIT 5
        ''')
        return cursor.fetchall()


    def check_high_score(self):
        print(f"Puntaje actual: {self.juego.score}")
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT nombre, MAX(puntaje) as high_score FROM jugadores
            ''')
            result = cursor.fetchone()
            high_score = result['high_score'] if result and 'high_score' in result else 0
            cursor.close()
        except Exception as e:
            print(f"Error al obtener el puntaje más alto: {e}")
            return

        print(f"Puntaje más alto antes: {high_score}")
        
        if self.juego.score > high_score:
            self.juego.high_score = self.juego.score
            self.prep_high_score()
            
            try:
                cursor = self.conn.cursor()
                cursor.execute('''
                    UPDATE jugadores
                    SET puntaje = %s
                    WHERE nombre = %s
                ''', (self.juego.high_score, self.juego.nombre))
                self.conn.commit()
                cursor.close()
            except Exception as e:
                print(f"Error al actualizar el puntaje más alto: {e}")

        print(f"Puntaje más alto después: {self.juego.high_score}")

    def muestra_puntaje(self):
        self.screen.blit(self.score_imagen, self.score_rect)
        self.screen.blit(self.highscore_imagen, self.highscore_rect)
        self.corazones.draw(self.screen)
    
    def prep_corazones(self):
        self.corazones = Group()
        for numero_corazones in range(self.juego.vidas_nave):
            corazon = Corazones(self.juego)
            corazon.rect.x = 10 + numero_corazones * corazon.rect.width #donde va a ir los corazones 
            corazon.rect.y = 22
            self.corazones.add(corazon)

    def cerrar_conexion(self):
        try:
            self.conn.close()
            print("Conexión cerrada correctamente.")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")