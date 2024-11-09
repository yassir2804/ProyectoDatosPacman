import pygame
from pygame import font, Surface, draw, KEYDOWN, K_UP, K_DOWN, K_RETURN
from Constantes import *


class MenuGameOver:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.opciones = ["Nuevo Juego", "Salir"]
        self.opcion_seleccionada = 0

        # Configuración del menú
        self.configurarFuente("Fuentes/PressStart2P-Regular.ttf", 20)
        ANCHO_MENU = 300
        ALTO_MENU = 200
        self.superficie = Surface((ANCHO_MENU, ALTO_MENU))
        self.superficie.fill(NEGRO)
        self.rect = self.superficie.get_rect()
        self.rect.center = (TAMANIOPANTALLA[0] // 2, TAMANIOPANTALLA[1] // 2)
        self.sonido_gameover = pygame.mixer.Sound("multimedia/gameover.wav")
        self.sonido_reproducido = False
        pygame.mixer.stop()

    def configurarFuente(self, ruta_fuente, tamano):
        """Configura la fuente para el menú."""
        self.fuente = font.Font(ruta_fuente, tamano)

    def dibujar(self, game_over_ganado=False):
        # Solo reproducir el sonido si no es game over por victoria y no se ha reproducido antes
        if not self.sonido_reproducido and not game_over_ganado:
            pygame.mixer.stop()
            self.sonido_gameover.play()
            self.sonido_reproducido = True

        # Oscurecer el fondo
        s = Surface(TAMANIOPANTALLA)
        s.set_alpha(128)
        s.fill(NEGRO)
        self.pantalla.blit(s, (0, 0))

        # Dibujar el menú
        draw.rect(self.superficie, NEGRO, self.superficie.get_rect())
        draw.rect(self.superficie, BLANCO, self.superficie.get_rect(), 2)

        # Dibujar texto "GAME OVER"
        texto_game_over = self.fuente.render("GAME OVER", True, AMARILLO if game_over_ganado else ROJO)
        rect_game_over = texto_game_over.get_rect()
        rect_game_over.centerx = self.superficie.get_width() // 2
        rect_game_over.y = 20
        self.superficie.blit(texto_game_over, rect_game_over)

        # Dibujar opciones
        for i, opcion in enumerate(self.opciones):
            color = AMARILLO if i == self.opcion_seleccionada else BLANCO
            texto = self.fuente.render(opcion, True, color)
            rect_texto = texto.get_rect()
            rect_texto.centerx = self.superficie.get_width() // 2
            rect_texto.y = 80 + i * 50
            self.superficie.blit(texto, rect_texto)

        self.pantalla.blit(self.superficie, self.rect)

    def manejar_evento(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
            elif event.key == K_DOWN:
                self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
            elif event.key == K_RETURN:
                self.sonido_reproducido = False
                return self.opciones[self.opcion_seleccionada]
        return None