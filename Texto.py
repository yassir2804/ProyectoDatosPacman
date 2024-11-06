import pygame
from Constantes import *
from Vector import Vector1

class Texto(object):
    def __init__(self, texto, color, x, y, tamaño, tiempo=None, id=None, visible=True):
        self.id = id
        self.texto = texto
        self.color = color
        self.tamaño = tamaño
        self.visible = visible
        self.posicion = Vector1(x, y)
        self.temporizador = 0
        self.duracion = tiempo
        self.etiqueta = None
        self.destruir = False
        self.configurarFuente("Fuentes/PressStart2P-Regular.ttf")
        self.crearEtiqueta()

    def configurarFuente(self, ruta_fuente):
        try:
            self.fuente = pygame.font.Font(ruta_fuente, self.tamaño)
        except:
            self.fuente = pygame.font.SysFont('Arial', self.tamaño)

    def crearEtiqueta(self):
        self.etiqueta = self.fuente.render(self.texto, 1, self.color)

    def setTexto(self, nuevo_texto):
        self.texto = str(nuevo_texto)
        self.crearEtiqueta()

    def renderizar(self, pantalla):
        if self.visible:
            x = self.posicion.x
            y = self.posicion.y
            pantalla.blit(self.etiqueta, (x, y))


class GrupoTexto(object):
    def __init__(self):
        self.proximo_id = 10
        self.todos_los_textos = {}
        self.configurarTextos()
        self.vidas = 3  # Número inicial de vidas
        self.cargar_imagen_vida()
        self.cargar_imagen_fruta()
        self.cerezas_comidas = 3  # Inicializa el contador de cerezas
        self.game_over_visible = False

    def cargar_imagen_vida(self):
        self.imagen_vida = pygame.image.load("multimedia/Vidas.png").convert_alpha()
        self.imagen_vida = pygame.transform.scale(self.imagen_vida, (45, 45))

    def cargar_imagen_fruta(self):
        self.imagen_fruta = pygame.image.load("multimedia/Cherry.png").convert_alpha()
        self.imagen_fruta = pygame.transform.scale(self.imagen_fruta, (45, 45))  # Escalar la imagen

    def agregarTexto(self, texto, color, x, y, tamaño, tiempo=None, id=None):
        self.proximo_id += 1
        self.todos_los_textos[self.proximo_id] = Texto(texto, color, x, y, tamaño, tiempo=tiempo, id=id)
        return self.proximo_id

    def configurarTextos(self):
        tamaño = ALTURACELDA
        self.todos_los_textos[SCORETXT] = Texto("0".zfill(8), BLANCO, 0, ALTURACELDA, tamaño)
        self.todos_los_textos[LEVELTXT] = Texto(str(1).zfill(3), BLANCO, 23 * ANCHOCELDA, ALTURACELDA, tamaño)
        self.todos_los_textos[READYTXT] = Texto("¡LISTO!", AMARILLO, 11.25 * ANCHOCELDA, 20 * ALTURACELDA, tamaño,
                                                visible=False)
        self.todos_los_textos[PAUSETXT] = Texto("¡PAUSA!", AMARILLO, 10.625 * ANCHOCELDA, 20 * ALTURACELDA, tamaño,
                                                visible=False)
        self.todos_los_textos[GAMEOVERTXT] = Texto("¡FIN DEL JUEGO!", AMARILLO, 10 * ANCHOCELDA, 20 * ALTURACELDA,
                                                   tamaño, visible=False)
        self.agregarTexto("PUNTOS", BLANCO, 0, 0, tamaño)
        self.agregarTexto("NIVEL", BLANCO, 23 * ANCHOCELDA, 0, tamaño)

    def actualizar(self, dt):
        for tkey in list(self.todos_los_textos.keys()):
            if self.todos_los_textos[tkey].destruir:
                self.todos_los_textos.pop(tkey)

    def actualizarPuntaje(self, puntaje):
        if SCORETXT in self.todos_los_textos:
            self.todos_los_textos[SCORETXT].setTexto(str(puntaje).zfill(8))

    def actualizarVidas(self, vidas):
        self.vidas = vidas

    def agregarFruta(self):
        self.cerezas_comidas += 1  # Incrementar la cantidad de cerezas comidas

    def renderizar(self, pantalla):
        # Renderizar todos los textos
        for tkey in list(self.todos_los_textos.keys()):
            self.todos_los_textos[tkey].renderizar(pantalla)

        # Renderizar las vidas (corazones)
        margen = 10
        separacion = 5
        for i in range(self.vidas):
            x = margen + i * (self.imagen_vida.get_width() + separacion)
            y = TAMANIOPANTALLA[1] - self.imagen_vida.get_height() - margen
            pantalla.blit(self.imagen_vida, (x, y))

        # Renderizar cerezas comidas en la esquina inferior derecha
        for i in range(self.cerezas_comidas):
            x = TAMANIOPANTALLA[0] - (margen + (i + 1) * (self.imagen_fruta.get_width() + separacion))
            y = TAMANIOPANTALLA[1] - self.imagen_fruta.get_height() - margen
            pantalla.blit(self.imagen_fruta, (x, y))

        # Mostrar el texto "GAME OVER" si es necesario
        if self.game_over_visible:
            if GAMEOVERTXT in self.todos_los_textos:
                self.todos_los_textos[GAMEOVERTXT].visible = True

    def mostrar_game_over(self):
        self.game_over_visible = True
