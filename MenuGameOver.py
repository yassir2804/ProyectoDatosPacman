import pygame
from pygame import font, Surface, draw, KEYDOWN, K_UP, K_DOWN, K_RETURN
from Constantes import *


class MenuGameOver:
    """
    Clase que maneja el menú de Game Over del juego.
    Muestra las opciones de 'Nuevo Juego' y 'Salir' cuando el jugador pierde o gana.
    """

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.opciones = ["Nuevo Juego", "Salir"]  # Opciones disponibles en el menú
        self.opcion_seleccionada = 0  # Índice de la opción seleccionada

        # Configuración visual del menú
        self.configurarFuente("Fuentes/PressStart2P-Regular.ttf", 20)
        ANCHO_MENU = 300
        ALTO_MENU = 200

        # Crear superficie para el menú
        self.superficie = Surface((ANCHO_MENU, ALTO_MENU))
        self.superficie.fill(NEGRO)

        # Configurar posición del menú (centrado en pantalla)
        self.rect = self.superficie.get_rect()
        self.rect.center = (TAMANIOPANTALLA[0] // 2, TAMANIOPANTALLA[1] // 2)

        # Configuración del sonido de Game Over
        self.sonido_gameover = pygame.mixer.Sound("multimedia/gameover.wav")
        self.sonido_reproducido = False  # Control para reproducir el sonido solo una vez
        pygame.mixer.stop()  # Detener cualquier sonido previo

    def configurarFuente(self, ruta_fuente, tamano):
        """
        Configura la fuente para el texto del menú.
        """
        self.fuente = font.Font(ruta_fuente, tamano)

    def dibujar(self, game_over_ganado=False):
        """
        Dibuja el menú de Game Over en la pantalla.
        """
        # Reproducir sonido de game over solo una vez y si no es por victoria
        if not self.sonido_reproducido and not game_over_ganado:
            pygame.mixer.stop()
            self.sonido_gameover.play()
            self.sonido_reproducido = True

        # Crear efecto de oscurecimiento del fondo
        s = Surface(TAMANIOPANTALLA)
        s.set_alpha(128)  # Establecer transparencia
        s.fill(NEGRO)
        self.pantalla.blit(s, (0, 0))

        # Dibujar el marco del menú
        draw.rect(self.superficie, NEGRO, self.superficie.get_rect())
        draw.rect(self.superficie, BLANCO, self.superficie.get_rect(), 2)  # Borde blanco

        # Configurar y dibujar el texto "GAME OVER"
        texto_game_over = self.fuente.render(
            "GAME OVER",
            True,
            AMARILLO if game_over_ganado else ROJO  # Amarillo si ganó, rojo si perdió
        )
        rect_game_over = texto_game_over.get_rect()
        rect_game_over.centerx = self.superficie.get_width() // 2
        rect_game_over.y = 20
        self.superficie.blit(texto_game_over, rect_game_over)

        # Dibujar las opciones del menú
        for i, opcion in enumerate(self.opciones):
            # La opción seleccionada se muestra en amarillo, las demás en blanco
            color = AMARILLO if i == self.opcion_seleccionada else BLANCO
            texto = self.fuente.render(opcion, True, color)
            rect_texto = texto.get_rect()
            rect_texto.centerx = self.superficie.get_width() // 2
            rect_texto.y = 80 + i * 50  # Espaciado vertical entre opciones
            self.superficie.blit(texto, rect_texto)

        # Dibujar el menú completo en la pantalla
        self.pantalla.blit(self.superficie, self.rect)

    def manejar_evento(self, event):
        """
        Maneja los eventos de teclado para navegar por el menú.
        """
        if event.type == KEYDOWN:
            if event.key == K_UP:
                # Mover selección hacia arriba (con wrap-around)
                self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
            elif event.key == K_DOWN:
                # Mover selección hacia abajo (con wrap-around)
                self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
            elif event.key == K_RETURN:
                # Resetear el control de sonido y retornar la opción seleccionada
                self.sonido_reproducido = False
                return self.opciones[self.opcion_seleccionada]
        return None