import pygame
from Vector import Vector1  # Importando Vector1 en lugar de Vector2
from Constantes import *
import numpy as np

class Pellet(object):
    def __init__(self, fila, columna):
        self.nombre = PELLET
        self.posicion = Vector1(columna * ANCHOCELDA, fila * ALTURACELDA)  # Cambiado a Vector1
        self.color = BLANCO
        self.radio = int(4 * ANCHOCELDA / 16)
        self.radioColision = int(4 * ANCHOCELDA / 16)
        self.puntos = 10
        self.visible = True

    def render(self, pantalla):
        if self.visible:
            p = self.posicion.entero()
            pygame.draw.circle(pantalla, self.color, p, self.radio)

class PelletPoder(Pellet):
    def __init__(self, fila, columna):
        Pellet.__init__(self, fila, columna)
        self.nombre = PELLETPODER
        self.radio = int(8 * ANCHOCELDA / 16)
        self.puntos = 50
        self.tiempoParpadeo = 0.2
        self.temporizador = 0

    def actualizar(self, dt):
        self.temporizador += dt
        if self.temporizador >= self.tiempoParpadeo:
            self.visible = not self.visible
            self.temporizador = 0

class GrupoPellets(object):
    def __init__(self, archivoPellets):
        self.listaPellets = []
        self.pelletsPoder = []
        self.crearListaPellets(archivoPellets)
        self.numComidos = 0

    def actualizar(self, dt):
        for pelletPoder in self.pelletsPoder:
            pelletPoder.actualizar(dt)

    def crearListaPellets(self, archivoPellets):
        datos = self.leerArchivoPellets(archivoPellets)
        for fila in range(datos.shape[0]):
            for col in range(datos.shape[1]):
                if datos[fila][col] in ['.', '+']:
                    self.listaPellets.append(Pellet(fila, col))
                elif datos[fila][col] in ['P', 'p']:
                    pp = PelletPoder(fila, col)
                    self.listaPellets.append(pp)
                    self.pelletsPoder.append(pp)

    def leerArchivoPellets(self, archivoTexto):
        return np.loadtxt(archivoTexto, dtype='<U1')

    def estaVacio(self):
        return len(self.listaPellets) == 0

    def render(self, pantalla):
        for pellet in self.listaPellets:
            pellet.render(pantalla)