import pygame
import numpy as np
from Vector import Vector1
from Constantes import *


class MapaRenderer:
    def __init__(self):
        self.tiempo_parpadeo = 0
        self.color = AZUL
        self.intervalo_parpadeo = 0.3
        self.parpadeo_activo = False
        self.grosor_linea = 2
        self.tamano_celda = 16
        self.TAMANO_PARED = 8
        self.OFFSET_X = -11  # Aumentamos el offset horizontal para mover más a la izquierda
        self.OFFSET_Y = -10  # Añadimos offset vertical para mover hacia arriba

    def es_pared(self, x, y):
        if 0 <= y < self.datos.shape[0] and 0 <= x < self.datos.shape[1]:
            return self.datos[y][x] == 'X'
        return True

    def es_casa_fantasmas(self, x, y):
        if 0 <= y < self.altura and 0 <= x < self.ancho:
            return self.datos[y][x] == '='
        return False

    def cargar_mapa(self, archivo):
        self.datos = np.loadtxt(archivo, dtype='<U1')
        self.altura = self.datos.shape[0]
        self.ancho = self.datos.shape[1]

    def actualizar(self, dt, modo_freight=False):
        if modo_freight:
            self.tiempo_parpadeo += dt
            if self.tiempo_parpadeo >= self.intervalo_parpadeo:
                self.parpadeo_activo = not self.parpadeo_activo
                self.tiempo_parpadeo = 0
        else:
            self.parpadeo_activo = False
            self.tiempo_parpadeo = 0

    def color_mapa(self, nivel):
        if nivel == 1:
            self.color = AZUL
        elif nivel == 2:
            self.color = ROJO
        elif nivel == 3:
            self.color = AMARILLO

    def tiene_pared_adyacente(self, x, y, direccion):
        dx, dy = 0, 0
        if direccion == 'arriba':
            dy = -1
        elif direccion == 'abajo':
            dy = 1
        elif direccion == 'izquierda':
            dx = -1
        elif direccion == 'derecha':
            dx = 1

        return self.es_pared(x + dx, y + dy)

    def render(self, superficie):
        color_actual = BLANCO if self.parpadeo_activo else self.color
        superficie.fill(NEGRO)

        # Recorremos el mapa para dibujar los perímetros
        for y in range(self.altura):
            for x in range(self.ancho):
                if self.es_pared(x, y):
                    # Aplicamos ambos offsets a las coordenadas
                    px = x * ANCHOCELDA + self.OFFSET_X
                    py = y * ALTURACELDA + self.OFFSET_Y

                    # Verificamos cada lado para ver si necesitamos dibujar una línea
                    # Línea superior
                    if not self.tiene_pared_adyacente(x, y, 'arriba'):
                        pygame.draw.line(superficie, color_actual,
                                         (px, py),
                                         (px + ANCHOCELDA, py),
                                         self.grosor_linea)

                    # Línea inferior
                    if not self.tiene_pared_adyacente(x, y, 'abajo'):
                        pygame.draw.line(superficie, color_actual,
                                         (px, py + ALTURACELDA),
                                         (px + ANCHOCELDA, py + ALTURACELDA),
                                         self.grosor_linea)

                    # Línea izquierda
                    if not self.tiene_pared_adyacente(x, y, 'izquierda'):
                        pygame.draw.line(superficie, color_actual,
                                         (px, py),
                                         (px, py + ALTURACELDA),
                                         self.grosor_linea)

                    # Línea derecha
                    if not self.tiene_pared_adyacente(x, y, 'derecha'):
                        pygame.draw.line(superficie, color_actual,
                                         (px + ANCHOCELDA, py),
                                         (px + ANCHOCELDA, py + ALTURACELDA),
                                         self.grosor_linea)

        # Dibujar la casa de los fantasmas
        for y in range(self.altura):
            for x in range(self.ancho):
                if self.es_casa_fantasmas(x, y):
                    px = x * ANCHOCELDA + self.OFFSET_X
                    py = y * ALTURACELDA + self.OFFSET_Y
                    pygame.draw.line(superficie, BLANCO,
                                     (px, py),
                                     (px + ANCHOCELDA, py),
                                     self.grosor_linea)