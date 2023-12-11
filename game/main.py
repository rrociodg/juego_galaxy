import pygame, sys 
import random
import time
import pygame.mixer
from nave import Nave
from disparo_nave import Bullet
from disparos_alien import AlienBullet
from aliens import Alien
from estadisticas import Estadisticas
from tabla_puntaje import TablaPuntajes
from time import sleep
from botones import Boton
from cronometro import Cronometro
from asteroides import Asteroide
from moneda import Moneda
from corazones import Corazones

class Galaxy:
    def __init__(self):
        pygame.init()
        self.score = 0
        self.high_score = 0
        self.ancho = 1150
        self.alto = 620
        self.screen = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Aventuras Espaciales")

        self.color = ((120, 40, 140))
        self.velocidad = 1
        self.anchobala = 3
        self.altobala = 15
        self.colorbala = (60, 60, 60)

        self.font = pygame.font.Font(None, 24) 
        self.color_texto = (255, 255, 255)

        self.anchobalaalien = 3
        self.altobalaalien = 15
        self.colorbalaalien = (255, 0, 0)  # Puedes ajustar el color según
        
        self.probabilidad_disparo_alien = 0.00020 
        
        #ASTEROIDES
        self.asteroides = pygame.sprite.Group()
        self.tiempo_asteroide = time.time()
        self.tiempo_objetivo = 8 # Los asteroides caen 

        #MONEDAS
        self.monedas = pygame.sprite.Group()
        self.tiempo_moneda = time.time()
        self.tiempo_objetivo_moneda = 5

        #CORAZON 
        self.corazones = pygame.sprite.Group()  # Grupo de sprites para los corazones
        self.tiempo_corazon = time.time()
        self.tiempo_objetivo_corazon = 10  # Los corazones 

        self.vidas_nave = 3 #vidas
        self.velocidad_nave = 1
        self.estadisticas = Estadisticas(self)
        self.tablaP = TablaPuntajes(self)
        self.nave = Nave(self)
        self.bullets = pygame.sprite.Group()
        self.balas_aliens = pygame.sprite.Group()
        self.balastotales = 9999999999999999999
        self.aliens = pygame.sprite.Group()
        
        self.velocidad_alien = 0.2
        self.flota_velocidad = 5
        self.flota_direccion = 1
        self.estado = "menu"
        self.juego_activado = False
        self.sonido_encendido = True  
        self.musica_encendida = True
        self._create_fleet()
        
        self.tabla_puntajes = TablaPuntajes(self)

        ruta_jugar = "JUEGO_FINAL.py/juego_2.py/recursos_galaxia/botones/start1.png"
        ruta_configuracion = "JUEGO_FINAL.py/juego_2.py/recursos_galaxia/botones/opciones1.png"
        ruta_puntaje = "JUEGO_FINAL.py/juego_2.py/recursos_galaxia/botones/score1.png"
        ruta_salir = "JUEGO_FINAL.py/juego_2.py/recursos_galaxia/botones/quit1.png"
        ruta_musica = "JUEGO_FINAL.py/juego_2.py/recursos_galaxia/botones/music.png"
        ruta_sonido = "JUEGO_FINAL.py/juego_2.py/recursos_galaxia/botones/sound.png"
        ruta_volver = "JUEGO_FINAL.py/juego_2.py/recursos_galaxia/botones/back1.png"

        self.menu_botones = [
            Boton(self, ruta_jugar, 450, 180),
            Boton(self, ruta_configuracion, 450, 280),
            Boton(self, ruta_puntaje, 450, 380),
            Boton(self, ruta_salir, 450, 480)
        ]
        self.opciones_botones = [
            Boton(self, ruta_musica, 450, 280),
            Boton(self, ruta_sonido, 450, 380),
            Boton(self, ruta_volver, 450, 480)
        ]

        self.play_boton = self.menu_botones[0]  # Botón "Jugar"
        self.config_boton = self.menu_botones[1]  # Botón "Configuración"
        self.puntaje_boton = self.menu_botones[2]  # Botón "Puntaje"
        self.salir_boton = self.menu_botones[3]  # Botón "Salir"

        self.musica_boton = self.opciones_botones[0]  #  "Música"
        self.sonido_boton = self.opciones_botones[1]  #  "Sonido"
        self.volver_boton = self.opciones_botones[2]  # Botón "Volver"
        self.valores_default()

        self.font_path = "JUEGO_FINAL.py/juego_2.py/recursos_galaxia/letras/GAMERIA.ttf"  
        self.title_font = pygame.font.Font(self.font_path, 72)


        self.fondo = pygame.image.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/fondos/fondo_espacio.jpg")
        self.fondo = pygame.transform.scale(self.fondo, (self.ancho, self.alto))

        #RELACIONADO CON EL CRONOMETRO 
        self.cronometro = Cronometro(self)  

        #RELACIONADO CON LA PANTALLA DE INICIO DE NIVELES  
        self.nivel = 1
        self.fondo_seleccionado = pygame.image.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/fondos/nivelesOK.jpg")
        self.font_path_niveles = "JUEGO_FINAL.py/juego_2.py/recursos_galaxia/letras/letraniveles.ttf" 
        self.title_font_niveles = pygame.font.Font(self.font_path, 72)
        self.title_font_subtitulo_niveles = pygame.font.Font(self.font_path, 20)
        self.texto_adicional = "Te perdiste en el espacio y debes completar 3 niveles para volver a tu hogar"

        #RELACIONADO CON EL FONDO DE LOS NIVELES 
        self.fondo_nivel_ = pygame.image.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/fondos/fondonivel1.jpg")
        self.fondo_nivel = pygame.transform.scale(self.fondo_nivel_, (self.ancho, self.alto))

        #RELACIONADO CON LA MUSICA 
        pygame.mixer.music.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/music1.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

        #RELACIONADO CON EL SONIDO DEL CLICK 
        self.sonido_click = pygame.mixer.Sound("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/click.mp3") 
        
    def dibuja_titulo(self):
        titulo = self.title_font.render("Aventuras Espaciales", True, (120, 40, 140))
        titulo_rect = titulo.get_rect()
        titulo_rect.centerx = self.ancho // 2
        titulo_rect.y = 50
        self.screen.blit(titulo, titulo_rect)
    
    def dibuja_fondo(self):
        # Dibuja el fondo de pantalla en la posición (0, 0)
        self.screen.blit(self.fondo, (0, 0))

    def dibuja_nivel(self):
        self.screen.blit(self.fondo_nivel, (0, 0))

    def solicitar_nombre(self):
        font = pygame.font.Font('JUEGO_FINAL.py/juego_2.py/recursos_galaxia/letras/gamer.ttf', 50) 
        color = pygame.Color((0, 0, 0))
        box = pygame.Rect(self.ancho // 2 - 220, self.alto // 2 - 50, 800, 90) 
        active = False
        text = ''
        fondo = pygame.image.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/fondos/fondo_espacio.jpg")
        fondo_escalado = pygame.transform.scale(fondo, (self.ancho, self.alto)) 
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            if text == '':
                                print('El nombre no puede estar vacío.')
                            elif not text.isalnum():
                                print('El nombre solo puede contener letras y números.')
                            else:
                                self.tablaP.guardar_puntaje(text, 0)
                                self.nombre_jugador = text
                                return
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill((0, 0, 0))
            self.screen.blit(fondo_escalado, (0, 0))  
            txt_surface = font.render(text, True, color)
            width = max(500, txt_surface.get_width()+10)
            box.w = width
            self.screen.blit(txt_surface, (box.x+5, box.y+5))
            pygame.draw.rect(self.screen, color, box, 2)

            prompt = font.render("Antes de jugar indicame tu nombre", True, (120, 40, 140))
            self.screen.blit(prompt, (170, 80))

            pygame.display.flip()

    def chequear_boton(self, mousePos):
        if self.estado == "menu":
            for boton in self.menu_botones:
                if boton.rect.collidepoint(mousePos):
                    self.handle_menu_button(boton)
                    break
        elif self.estado == "opciones":
            for boton in self.opciones_botones:
                if boton.rect.collidepoint(mousePos):
                    self.handle_options_button(boton)
                    break

    def handle_menu_button(self, boton):
        if boton == self.play_boton and not self.juego_activado:
            self.mostrar_mensaje("NIVEL UNO", 2)
            self.mostrar_mensaje_adicional(self.texto_adicional, 4)
            self.estado = "juego"
            self.juego_activado = True
            
        elif boton == self.config_boton and not self.juego_activado:
            print("Ir a configuración")
            self.estado = "opciones"
        elif boton == self.puntaje_boton and not self.juego_activado:
            self.mostrar_top_jugadores()  # Muestra los puntajes
            pygame.display.flip()
            print("Ver puntaje")
        elif boton == self.salir_boton and not self.juego_activado:
            pygame.quit()
            quit()

    def handle_options_button(self, boton):
        if boton == self.musica_boton and self.estado == "opciones":
            if self.musica_encendida:
                print("Apagar música")
                pygame.mixer.music.stop()
                self.musica_encendida = False
            else:
                print("Encender música")
                pygame.mixer.music.load("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/music1.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)
                self.musica_encendida = True
        elif boton == self.sonido_boton and self.estado == "opciones":
            if self.sonido_encendido:
                print("Apagar sonido")
                self.sonido_encendido = False
            else:
                print("Encender sonido")
                self.sonido_encendido = True
            self.reproducir_sonido_click()
        elif boton == self.volver_boton and self.estado == "opciones":
            print("Volver al menú principal")
            self.estado = "menu"
            self.juego_activado = False
            self.screen.fill((0, 0, 0))  # Limpia la pantalla
            self.dibuja_fondo()
            for boton in self.menu_botones:
                boton.dibuja_boton()
            pygame.display.flip()  # Actualiza la pantalla

    def corre_juego(self):
        self.solicitar_nombre()
        puntaje_guardado = False
        while True:
            tiempo_actual = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()   
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.nave.mover_derecha = True 
                    if event.key == pygame.K_LEFT:
                        self.nave.mover_izquierda = True
                    if event.key == pygame.K_SPACE:
                        self._fire_bullet()
                        self.cronometro.iniciar_cronometro()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.nave.mover_derecha = False
                    if event.key == pygame.K_LEFT:
                        self.nave.mover_izquierda = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    self.chequear_boton(mousePos) # Marca que el evento ha sido manejado
                    if self.sonido_encendido:
                        self.reproducir_sonido_click()  # Reproduce el sonido de clic

            if self.juego_activado:
                self.nave.mover()
                self.dibuja_nivel()
                self.nave.corre()
                self.bullets.update()
                self.update_alien()
                self.cronometro.iniciar_cronometro()
                self.cronometro.mostrar_cronometro()

                if tiempo_actual - self.tiempo_asteroide >= self.tiempo_objetivo:
                    asteroide = Asteroide(self)
                    self.asteroides.add(asteroide)
                    self.tiempo_asteroide = tiempo_actual  # contador de tiempo de los asteroides

                if tiempo_actual - self.tiempo_moneda >= self.tiempo_objetivo_moneda:
                    moneda = Moneda(self)
                    self.monedas.add(moneda)
                    self.tiempo_moneda = tiempo_actual  #  contador de tiempo de las monedas

                if tiempo_actual - self.tiempo_corazon >= self.tiempo_objetivo_corazon:
                    corazon = Corazones(self)
                    self.corazones.add(corazon)
                    self.tiempo_corazon = tiempo_actual  # contador de tiempo de los corazones

                for bullet in self.bullets.copy():
                    if bullet.rect.bottom <= 0:
                        self.bullets.remove(bullet)
                    
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                    
                self.aliens.draw(self.screen)   
                self.tablaP.muestra_puntaje() 

                self.asteroides.update()
                self.asteroides.draw(self.screen)

                self.corazones.update() 
                self.corazones.draw(self.screen)  

                corazones_colisionados = pygame.sprite.spritecollide(self.nave, self.corazones, True)

                for corazon in corazones_colisionados:
                    self.vidas_nave += 1
                    self.tablaP.prep_corazones()

                if pygame.sprite.spritecollideany(self.nave, self.asteroides):
                    self.vidas_nave -= 1
                    self.cronometro.detener_cronometro()
                    if self.vidas_nave <= 0:
                        self.mostrar_pantalla_perdedor()
                        pygame.quit()
                        sys.exit()
                    else:
                        self.mostrar_pantalla_perdedor()

                if not self.juego_activado and self.vidas_nave <= 0: 
                    if not puntaje_guardado:
                        self.tablaP.guardar_puntaje(self.nombre_jugador, self.score)
                        puntaje_guardado = True
                    self.finalizar_juego()  
                    self.mostrar_pantalla_perdedor() 
                    self.tablaP.cerrar_conexion()  # Cierra la conexión después de usarla 
                    pygame.quit() 
                    sys.exit() 

                self.monedas.update()
                self.monedas.draw(self.screen)

                monedas_recolectadas = pygame.sprite.spritecollide(self.nave, self.monedas, True)

                for moneda in monedas_recolectadas:
                    self.score += 150  # Aumenta la puntuación 
                    self.tablaP.prep_score()

                for alien_bullet in self.balas_aliens.copy():
                    alien_bullet.update()
                    alien_bullet.draw_bullet()
                
                self.cronometro.mostrar_cronometro()
                
                pygame.display.flip()

            else:
                self.mouse_event_handled = False  # Restablece el control 
                self.screen.fill((0, 0, 0))  # Limpia la pantalla
                self.dibuja_fondo()
            
                self.dibuja_titulo()

                self.cronometro.detener_cronometro()

                if self.estado == "menu":
                    for boton in self.menu_botones:
                        boton.dibuja_boton()
                elif self.estado == "opciones":
                    for boton in self.opciones_botones:
                        boton.dibuja_boton()
            
                pygame.display.flip()

            pygame.display.flip()


    def mostrar_top_jugadores(self):
        # Obtén los mejores jugadores
        top_jugadores = self.tablaP.obtener_top_jugadores()

        # Define la posición inicial donde se mostrará el título
        x_titulo = self.ancho // 2
        y_titulo = self.alto // 8  # Ajusta esta posición según tus preferencias

        # Define la fuente y el tamaño del texto del título
        font_titulo = pygame.font.Font(None, 48)
        color_titulo = (200, 0, 255)  # Color violeta

        # Limpia la pantalla
        self.screen.fill((0, 0, 0))
        self.dibuja_fondo()
        self.dibuja_titulo()

        # Dibuja el título de la tabla de puntajes
        titulo = font_titulo.render("Top 5 Jugadores", True, color_titulo)
        titulo_rect = titulo.get_rect()
        titulo_rect.centerx = x_titulo
        titulo_rect.y = y_titulo
        self.screen.blit(titulo, titulo_rect)

        # Define la posición inicial donde se mostrarán los jugadores
        x_jugadores = self.ancho // 2 - 150
        y_jugadores = y_titulo + 60  # Ajusta esta posición según tus preferencias

        # Define la fuente y el tamaño del texto de los jugadores
        font_jugadores = pygame.font.Font(None, 36)
        color_jugadores = (255, 255, 255)  # Color blanco

        # Recorre la lista de los mejores jugadores
        for jugador in top_jugadores:
            # Crea el texto con el nombre del jugador y su puntuación
            texto = f"{jugador[0]}: {jugador[1]}"  # Accede a los elementos de la tupla por índice

            # Renderiza el texto
            txt_surface = font_jugadores.render(texto, True, color_jugadores)

            # Muestra el texto en la pantalla
            self.screen.blit(txt_surface, (x_jugadores, y_jugadores))

            # Actualiza la posición y para el próximo jugador
            y_jugadores += 40

        # Muestra el botón de volver
        self.volver_boton.dibuja_boton()

        # Actualiza la pantalla
        pygame.display.flip()

        # Espera hasta que se presione el botón de volver
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.volver_boton.rect.collidepoint(mouse_pos):
                        # Volver al menú principal
                        self.estado = "menu"
                        self.juego_activado = False
                        return
                    


    def reiniciar_juego(self):
    # Restablece todas las variables del juego a su estado inicial
        self.score = 0
        self.high_score = 0
        self.vidas_nave = 3
        self.velocidad_nave = 1
        self.velocidad_alien = 0.5
        self.flota_direccion = 1
        self.nivel = 1 
        # Restablecer cualquier otra variable o configuración que necesite ser reiniciada
        # Volver a crear la flota de aliens
        self.aliens.empty()
        self.bullets.empty()
        self.balas_aliens.empty()
        self.asteroides.empty()
        self.monedas.empty()
        self.corazones.empty()
        self._create_fleet()
        self.nave = Nave(self)  # Crea una nueva nave

        # Volver a iniciar el juego
        self.juego_activado = True
        self.estado = "juego"
        self.mostrar_mensaje("NIVEL UNO", 2)

    def mostrar_pantalla_ganador(self):
        fondo = pygame.image.load('JUEGO_FINAL.py/juego_2.py/recursos_galaxia/fondos/fondoganar.jpg')  
        fondo = pygame.transform.scale(fondo, (self.ancho, self.alto))  
        self.screen.blit(fondo, (0, 0))  

        font = pygame.font.Font("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/letras/GAMERIA.ttf" , 30)
        text = font.render("Lograste superar los niveles y pudiste llegar a tu hogar", True, (0, 0, 0))
        self.screen.blit(text, (self.ancho // 2 - text.get_width() // 2, self.alto // 4 - text.get_height() // 2))

        boton_volver_a_jugar = pygame.Rect(self.ancho // 2 - 100, self.alto // 2 + 50, 200, 30)
        boton_highscore = pygame.Rect(self.ancho // 2 - 100, self.alto // 2 + 150, 200, 30)  
        boton_salir = pygame.Rect(self.ancho // 2 - 100, self.alto // 2 + 250, 200, 30)

        text_volver_a_jugar = font.render("Volver a jugar", True, (0, 0, 0))
        self.screen.blit(text_volver_a_jugar, (self.ancho // 2 - text_volver_a_jugar.get_width() // 2, self.alto // 2 + 50 + text_volver_a_jugar.get_height() // 2))

        # text_highscore = font.render("Highscore", True, (0, 0, 0))  
        # self.screen.blit(text_highscore, (self.ancho // 2 - text_highscore.get_width() // 2, self.alto // 2 + 150 + text_highscore.get_height() // 2))

        text_salir = font.render("Salir", True, (0, 0, 0))
        self.screen.blit(text_salir, (self.ancho // 2 - text_salir.get_width() // 2, self.alto // 2 + 250 + text_salir.get_height() // 2))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # Obtiene la posición del mouse
                    if boton_volver_a_jugar.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        return
                    elif boton_highscore.collidepoint(mouse_pos):
                        self.mostrar_puntajes()
                        return  # Agregado para salir del bucle después de mostrar puntajes
                    elif boton_salir.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()


    def mostrar_pantalla_perdedor(self):
        fondo = pygame.image.load('JUEGO_FINAL.py/juego_2.py/recursos_galaxia/fondos/perdedor.jpg')
        fondo = pygame.transform.scale(fondo, (self.ancho, self.alto))
        self.screen.blit(fondo, (0, 0))

        font = pygame.font.Font("JUEGO_FINAL.py/juego_2.py/recursos_galaxia/letras/GAMERIA.ttf" , 31)
        text = font.render("No pudiste llegar a la tierra pero te invito a volver a jugar", True, (255, 255, 255))
        self.screen.blit(text, (self.ancho // 2 - text.get_width() // 2, self.alto // 4 - text.get_height() // 2))

        boton_volver_a_jugar = pygame.Rect(self.ancho // 2 - 100, self.alto // 2 + 100, 200, 50)
        boton_salir = pygame.Rect(self.ancho // 2 - 100, self.alto // 2 + 200, 200, 50)

        text_volver_a_jugar = font.render("Volver a jugar", True, (255, 255, 255))
        self.screen.blit(text_volver_a_jugar, (self.ancho // 2 - text_volver_a_jugar.get_width() // 2, self.alto // 2 + 100 + text_volver_a_jugar.get_height() // 2))

        text_salir = font.render("Salir", True, (255, 255, 255))
        self.screen.blit(text_salir, (self.ancho // 2 - text_salir.get_width() // 2, self.alto // 2 + 200 + text_salir.get_height() // 2))  

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # Obtiene la posición del mouse
                    if boton_volver_a_jugar.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        return
                    elif boton_salir.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()

    def reproducir_sonido_click(self):
        self.sonido_click.play()

    def _fire_bullet(self):
        if self.balastotales != 0:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.balastotales = self.balastotales - 1

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space = self.ancho - (2 * alien_width)
        numero_aliens = available_space // (2 * alien_width)
        nave_height = self.nave.rect.height
        available_space_y = self.alto - (3 * alien_height) - nave_height
        numero_filas = available_space_y // (2 * alien_height) #un alien y un espacio 

        for fila in range(numero_filas):
            for numero_alien in range(numero_aliens):
                self._create_alien(numero_alien, fila)

    def _create_alien(self, numero_alien, fila):
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * numero_alien
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * fila
            self.aliens.add(alien)  

    def alien_disparar(self, alien):
        nueva_bala_alien = AlienBullet(self, alien)
        self.balas_aliens.add(nueva_bala_alien)

    def chequear_bordes_flota(self):
        for alien in self.aliens.sprites():
            if alien.chequear_bordes():
                self.cambia_direccion()
                break

    def cambia_direccion(self):
        for alien in self.aliens.sprites():     
            alien.rect.y += self.flota_velocidad
        self.flota_direccion *= -1        

    def update_alien(self):
        self.chequear_bordes_flota()
        self.aliens.update()
        if not self.aliens:
            self.bullets.empty()
            self.aumenta_velocidad()
            self._create_fleet()

            self.nivel += 1
        
            if self.nivel == 4:
                self.mostrar_pantalla_ganador()
                return

            self.mostrar_mensaje("NIVEL " + str(self.nivel), 2)  

        colisiones = pygame.sprite.spritecollide(self.nave, self.balas_aliens, True)
        if colisiones:
            self.nave_colisionada()

        for alien in self.aliens.sprites():
            alien.update()

            # Agrega lógica de disparo de los aliens después de actualizar todos los aliens
            if random.random() < self.probabilidad_disparo_alien: 
                self.alien_disparar(alien)

        # Verifica si alguna bala alienígena ha colisionado con la nave
        if pygame.sprite.spritecollideany(self.nave, self.balas_aliens):
            self.nave_colisionada()

    """Este método establece los valores iniciales para la velocidad de la nave, las balas y 
    los aliens, así como la dirección de la flota de aliens. 
    Se utiliza para configurar el estado inicial del juego."""
    def valores_default(self):
        self.velocidad_nave = 1
        self.velocidad = 1
        self.velocidad_alien = 1.0

        self.flota_direccion = 0.5 #modifica la velocidad de los aliens 

    def aumenta_velocidad(self):
        self.velocidad_nave += 0.1  # Aumenta la velocidad de la nave 
        self.velocidad += 0.2  # Aumenta la velocidad de las balas
        self.velocidad_alien += 0.2  # Aumenta la velocidad de los aliens 
        self.tiempo_objetivo *= 0.9

    def nave_colisionada(self):
        if self.vidas_nave > 0:
            self.vidas_nave -= 1
            self.tablaP.prep_corazones()    

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.nave.centrar_nave()
            # self.score += 10

            sleep(0.5)
        else:
            self.juego_activado = False 
            self.cronometro.detener_cronometro()

    def mostrar_mensaje(self, mensaje, duracion):
        fondo_ajustado = pygame.transform.scale(self.fondo_seleccionado, (self.ancho, self.alto))
        self.screen.blit(fondo_ajustado, (0, 0))
        text = self.title_font_niveles.render(mensaje, True, (0, 0, 0))  # Crea el texto
        rect = text.get_rect()  # Obtiene el rectángulo que encierra al texto
        rect.center = (self.ancho / 2, self.alto / 2)  # Centra el rectángulo
        self.screen.blit(text, rect)  # Dibuja el texto en la pantalla

        # Actualiza la pantalla y pausa el juego por un momento
        pygame.display.flip()
        pygame.time.wait(duracion * 1000)

    def mostrar_mensaje_adicional(self, mensaje, duracion):
        fuente = pygame.font.Font(None, 29)
        texto = self.title_font_subtitulo_niveles.render(mensaje, True, (0, 0, 0))
        rectangulo = texto.get_rect()
        rectangulo.center = (self.ancho // 2, self.alto // 2 + 50)
        self.screen.blit(texto, rectangulo)

        mensaje_adicional = "No dejes que te toquen los asteroides sino vas a morir"
        texto_adicional = self.title_font_subtitulo_niveles.render(mensaje_adicional, True, (0, 0, 0))
        rectangulo_adicional = texto_adicional.get_rect()
        rectangulo_adicional.center = (self.ancho // 2, self.alto // 2 + 80)  # Ajusta la posición en y para que esté debajo del mensaje anterior
        self.screen.blit(texto_adicional, rectangulo_adicional)
        pygame.display.flip()
        time.sleep(duracion)


if __name__ == "__main__":
    a = Galaxy()
    a.corre_juego()
    tiempo_transcurrido = a.cronometro.obtener_tiempo_transcurrido()
    print(f"Tiempo transcurrido: {tiempo_transcurrido} segundos") 