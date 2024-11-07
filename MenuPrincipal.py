import pygame
from pygame.locals import *
from Main import Controladora
from Texto import Texto, GrupoTexto
from Constantes import *

# Definir un nuevo color azul claro
AZUL_CLARO = (173, 216, 230)

class MenuPrincipal:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMANIOPANTALLA, 0, 32)
        pygame.display.set_caption("PACMAN BY SAUL - YASSIR - MANUEL - ANGEL")
        self.fondo = pygame.surface.Surface(TAMANIOPANTALLA).convert()
        self.fondo.fill(NEGRO)
        self.clock = pygame.time.Clock()

        # Inicializar fuente
        self.fuente = pygame.font.Font("Fuentes/PressStart2P-Regular.ttf", 35)

        # Cargar la imagen del fondo
        self.imagen_fondo = pygame.image.load("multimedia/fototigrepacman.png")

        # Calcular posiciones centradas
        ancho_pantalla = TAMANIOPANTALLA[0]
        altura_pantalla = TAMANIOPANTALLA[1]

        # Posiciones para los textos
        self.pos_empezar = (ancho_pantalla // 2, altura_pantalla // 2 + 170)
        self.pos_cargar = (ancho_pantalla // 2, altura_pantalla // 2 + 200)

        # Crear textos del menú
        self.texto_start = TextoMenu("EMPEZAR", self.pos_empezar, self.fuente, color=AZUL_CLARO)
        self.texto_load = TextoMenu("CARGAR PARTIDA", self.pos_cargar, self.fuente, color=AZUL_CLARO)
        self.texto_seleccionado = self.texto_start

        # Cargar música de fondo
        self.musica_fondo = pygame.mixer.Sound("multimedia/musicapacman.wav")
        self.musica_fondo.set_volume(0.5)
        self.musica_fondo.play(-1)

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.texto_seleccionado = self.texto_start
                elif event.key == K_DOWN:
                    self.texto_seleccionado = self.texto_load
                elif event.key == K_RETURN:
                    if self.texto_seleccionado == self.texto_start:
                        self.iniciar_juego()
                    elif self.texto_seleccionado == self.texto_load:
                        self.cargar_partida()

        # Manejar hover del mouse
        pos_mouse = pygame.mouse.get_pos()
        self.texto_start.actualizar_hover(pos_mouse)
        self.texto_load.actualizar_hover(pos_mouse)

        # Manejar click del mouse
        if pygame.mouse.get_pressed()[0]:  # Click izquierdo
            if self.texto_start.hover:
                self.iniciar_juego()
            elif self.texto_load.hover:
                self.cargar_partida()

    def actualizar(self):
        self.manejar_eventos()

        # Limpiar pantalla
        self.pantalla.fill(NEGRO)

        # Dibujar la imagen de fondo
        self.pantalla.blit(self.imagen_fondo, (0, 0))

        # Dibujar textos
        self.texto_start.dibujar(self.pantalla, self.texto_seleccionado == self.texto_start)
        self.texto_load.dibujar(self.pantalla, self.texto_seleccionado == self.texto_load)

        pygame.display.update()

    def iniciar_juego(self):
        self.musica_fondo.stop()
        juego = Controladora()
        juego.empezar()
        while True:
            juego.actualizar()

    def cargar_partida(self):
        print("Cargando partida guardada...")
        self.musica_fondo.stop()
        juego = Controladora()
        if juego.cargar_estado("pacman_save.json"):
            juego.empezar()
            while True:
                juego.actualizar()
        else:
            print("Error al cargar la partida guardada.")



class TextoMenu:
    def __init__(self, texto, posicion, fuente, color=AZUL_CLARO):
        self.texto = texto
        self.posicion = posicion
        self.fuente = fuente
        self.color_normal = color
        self.color_hover = BLANCO
        self.borde_color = NEGRO  # Color del borde
        self.hover = False

        # Crear superficie de texto y definir el rectángulo de colisión
        self.superficie = self.fuente.render(self.texto, True, self.color_normal)
        self.rect = self.superficie.get_rect(center=self.posicion)

    def actualizar_hover(self, pos_mouse):
        self.hover = self.rect.collidepoint(pos_mouse)

    def dibujar(self, superficie, seleccionado):
        color = self.color_hover if self.hover or seleccionado else self.color_normal
        texto_surf = self.fuente.render(self.texto, True, color)

        # Crear el borde alrededor del texto
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:  # Borde en las esquinas
            borde_surf = self.fuente.render(self.texto, True, self.borde_color)
            superficie.blit(borde_surf, texto_surf.get_rect(center=(self.posicion[0] + dx, self.posicion[1] + dy)))

        # Dibujar el texto principal encima
        superficie.blit(texto_surf, texto_surf.get_rect(center=self.posicion))


if __name__ == '__main__':
    menu = MenuPrincipal()
    while True:
        menu.actualizar()
