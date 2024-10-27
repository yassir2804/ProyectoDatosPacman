import numpy as np
import pygame
from Vector import Vector1
from Constantes import *

class Nodo(object):
    def __init__(self, posicion):
        self.posicion = posicion
        self.vecinos = {
            DERECHA: None,
            IZQUIERDA: None,
            ARRIBA: None,
            ABAJO: None,
            PORTAL: None
        }

    def render(self, pantalla):
        for n in self.vecinos.keys():
            if self.vecinos[n] is not None:
                pygame.draw.line(pantalla, BLANCO, self.posicion.tupla(), self.vecinos[n].posicion.tupla())
        pygame.draw.circle(pantalla, ROJO, self.posicion.entero(), 12)

    def agregar_vecino(self, direccion, nodo_vecino):
        self.vecinos[direccion] = nodo_vecino

class Grafo(object):
    def __init__(self, nivel):
        self.nodosLUT = {}
        self.simbolosNodos = ['+']
        self.simbolosCaminos = ['.']
        datos = self.leer_laberinto(nivel)
        self.crear_tabla_nodos(datos)
        self.conectar_horizontal(datos)
        self.conectar_vertical(datos)

    def render(self, pantalla):
        for nodo in self.nodosLUT.values():
            nodo.render(pantalla)

    def leer_laberinto(self, archivoTexto):
        return np.loadtxt(archivoTexto, dtype='<U1')


    def crear_tabla_nodos(self, datos, xbalance=0, ybalance=0):
        for fila in range(datos.shape[0]):
            for col in range(datos.shape[1]):
                if datos[fila][col] in self.simbolosNodos:
                    x, y = self.construir_clave(col + xbalance, fila + ybalance)
                    self.nodosLUT[(x, y)] = Nodo(Vector1(x, y))

    def construir_clave(self, col, fila):
        return col * ANCHOCELDA, fila * ALTURACELDA

    def conectar_horizontal(self, datos):
        for fila in range(datos.shape[0]):
            key = None
            for col in range(datos.shape[1]):
                if datos[fila][col] in self.simbolosNodos:
                    if key is None:
                        key = self.construir_clave(col, fila)
                    else:
                        otrallave = self.construir_clave(col, fila)
                        self.nodosLUT[key].vecinos[DERECHA] = self.nodosLUT[otrallave]
                        self.nodosLUT[otrallave].vecinos[IZQUIERDA] = self.nodosLUT[key]
                        key = otrallave
                elif datos[fila][col] not in self.simbolosCaminos:
                    key = None

    def conectar_vertical(self, datos):
        datos_transpuestos = datos.transpose()
        for col in range(datos_transpuestos.shape[0]):
            key = None
            for fila in range(datos_transpuestos.shape[1]):
                if datos_transpuestos[col][fila] in self.simbolosNodos:
                    if key is None:
                        key = self.construir_clave(col, fila)
                    else:
                        otrallave = self.construir_clave(col, fila)
                        self.nodosLUT[key].vecinos[ABAJO] = self.nodosLUT[otrallave]
                        self.nodosLUT[otrallave].vecinos[ARRIBA] = self.nodosLUT[key]
                        key = otrallave
                elif datos_transpuestos[col][fila] not in self.simbolosCaminos:
                    key = None

    def obtener_nodo_desde_pixeles(self, pixel_x, pixel_y):
        if (pixel_x, pixel_y) in self.nodosLUT.keys():
            return self.nodosLUT[(pixel_x, pixel_y)]
        return None

    def obtener_nodo_desde_tiles(self, col, fila):
        clave = self.construir_clave(col, fila)
        return self.nodosLUT.get(clave, None)

    def punto_partida_pacman(self):
        return next(iter(self.nodosLUT.values()), None)

    def set_portales(self, par1, par2):
        clave1 = self.construir_clave(*par1)  # Corrección del nombre
        clave2 = self.construir_clave(*par2)  # Corrección del nombre
        if clave1 in self.nodosLUT.keys() and clave2 in self.nodosLUT.keys():  # Corrección de variable
            self.nodosLUT[clave1].vecinos[PORTAL] = self.nodosLUT[clave2]  # Asignación correcta
            self.nodosLUT[clave2].vecinos[PORTAL] = self.nodosLUT[clave1]  # Asignación correcta
