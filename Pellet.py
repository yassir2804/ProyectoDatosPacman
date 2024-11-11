import pygame
from Vector import Vector1
from Constantes import *
import numpy as np


class Pellet:
    """
    Clase base que representa los puntos (pellets) que Pac-Man puede comer.
    Son los objetos básicos de puntuación en el juego.
    """

    def __init__(self, fila, columna):
        """
        Inicializa un pellet básico.
        """
        self.nombre = PELLET
        # Convierte la posición de cuadrícula a píxeles
        self.posicion = Vector1(columna * ANCHOCELDA, fila * ALTURACELDA)
        self.color = BLANCO
        # Radio visual y de colisión proporcional al tamaño de la celda
        self.radio = int(4 * ANCHOCELDA / 16)
        self.radioColision = int(4 * ANCHOCELDA / 16)
        self.puntos = 10
        self.visible = True

    def render(self, pantalla):
        if self.visible:
            p = self.posicion.entero()
            pygame.draw.circle(pantalla, self.color, p, self.radio)


class PelletPoder(Pellet):
    """
    Pellet especial que otorga a Pac-Man la habilidad de comer fantasmas.
    Hereda de la clase Pellet pero tiene características adicionales.
    """

    def __init__(self, fila, columna):
        super().__init__(fila, columna)
        self.nombre = PELLETPODER
        self.radio = int(8 * ANCHOCELDA / 16)  # Radio más grande que el pellet normal
        self.puntos = 50  # Más puntos que el pellet normal
        # Atributos para el efecto de parpadeo
        self.tiempoParpadeo = 0.2
        self.temporizador = 0

    def actualizar(self, dt):
        self.temporizador += dt
        if self.temporizador >= self.tiempoParpadeo:
            self.visible = not self.visible  # Alterna visibilidad
            self.temporizador = 0


class GrupoPellets:
    """
    Gestiona todos los pellets del nivel como una colección.
    Maneja la creación, actualización y renderizado de todos los pellets.
    """

    def __init__(self, archivo_pellets):
        """
        Inicializa el grupo de pellets desde un archivo.
        """
        self.listaPellets = []  # Todos los pellets (normales y poder)
        self.pelletsPoder = []  # Solo power pellets
        self.crear_lista_pellets(archivo_pellets)
        self.numComidos = 0  # Contador de pellets comidos

    def actualizar(self, dt):
        for pelletPoder in self.pelletsPoder:
            pelletPoder.actualizar(dt)

    def crear_lista_pellets(self, archivo_pellets):
        """
        Crea los pellets basándose en el archivo de nivel.

        Args:
            archivo_pellets (str): Ruta al archivo con el layout de pellets

        Símbolos del archivo:
            '.' o '+': Pellet normal
            'P' o 'p': Power Pellet
        """
        datos = self.leer_archivo_pellets(archivo_pellets)
        for fila in range(datos.shape[0]):
            for col in range(datos.shape[1]):
                if datos[fila][col] in ['.', '+']:
                    self.listaPellets.append(Pellet(fila, col))
                elif datos[fila][col] in ['P', 'p']:
                    pp = PelletPoder(fila, col)
                    self.listaPellets.append(pp)
                    self.pelletsPoder.append(pp)

    def leer_archivo_pellets(self, archivo_texto):
        """
        Lee el archivo que define la disposición de pellets.
        """
        return np.loadtxt(archivo_texto, dtype='<U1')

    def esta_vacio(self):
        """
        Verifica si quedan pellets por comer.
        """
        return len(self.listaPellets) == 0

    def render(self, pantalla):

        for pellet in self.listaPellets:
            pellet.render(pantalla)