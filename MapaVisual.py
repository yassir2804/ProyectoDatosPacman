import pygame
import numpy as np
from Vector import Vector1
from Constantes import *


class NodoMapa:
    def __init__(self, x, y, tipo):
        self.posicion = Vector1(x, y)
        self.tipo = tipo
        self.tiene_pared = {
            'arriba': False,
            'abajo': False,
            'izquierda': False,
            'derecha': False
        }
        self.es_esquina = {
            'superior-izquierda': False,
            'superior-derecha': False,
            'inferior-izquierda': False,
            'inferior-derecha': False
        }


class MapaRenderer:
    def __init__(self):
        self.tiempo_parpadeo = 0
        self.color=AZUL
        self.intervalo_parpadeo = 0.3
        self.parpadeo_activo = False
        self.grosor_linea = 1  # Línea más delgada para la cuadrícula
        self.tamano_celda = 16  # Tamaño de cada celda de la cuadrícula
        self.TAMANO_PARED = 8  # Reducimos el tamaño de las paredes para hacer el camino más grande

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

    def color_mapa(self,nivel):
        if nivel ==1:
            self.color=AZUL
            if nivel==2:
                self.color=ROJO
        elif nivel==3:
            self.color=AMARILLO

    def render(self, superficie):
        color_actual = BLANCO if self.parpadeo_activo else self.color

        # Primero dibujamos el fondo negro para todo el mapa
        superficie.fill(NEGRO)

        # Dibujar las paredes como bloques sólidos pero más pequeños
        for y in range(self.altura):
            for x in range(self.ancho):
                if self.es_pared(x, y):
                    # Posición de la celda
                    px = x * ANCHOCELDA
                    py = y * ALTURACELDA

                    # Calculamos el offset para centrar la pared más pequeña en la celda
                    offset_x = (ANCHOCELDA - self.TAMANO_PARED) // 2
                    offset_y = (ALTURACELDA - self.TAMANO_PARED) // 2

                    # Dibujar un rectángulo más pequeño para cada celda de pared
                    pygame.draw.rect(superficie, color_actual,
                                     (px + offset_x, py + offset_y,
                                      self.TAMANO_PARED, self.TAMANO_PARED))

        # Dibujar la casa de los fantasmas (líneas blancas)
        for y in range(self.altura):
            for x in range(self.ancho):
                if self.es_casa_fantasmas(x, y):
                    px = x * ANCHOCELDA * 2
                    py = y * ALTURACELDA * 2
                    pygame.draw.line(superficie, BLANCO,
                                     (px, py),
                                     (px + ANCHOCELDA, py),
                                     self.grosor_linea)