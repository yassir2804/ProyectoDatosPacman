import pygame
import numpy as np
from Constantes import *


class MapaRenderer:
    """
    Clase encargada de renderizar el mapa del juego Pacman.
    Maneja la carga, procesamiento y visualización del laberinto.
    """

    def __init__(self):
        # Variables para control del efecto de parpadeo
        self.tiempo_parpadeo = 0  # Contador para el tiempo de parpadeo
        self.color = AZUL  # Color por defecto del mapa
        self.intervalo_parpadeo = 0.3  # Tiempo entre cada parpadeo
        self.parpadeo_activo = False  # Estado actual del parpadeo

        # Configuración visual del mapa
        self.grosor_linea = 2  # Grosor de las paredes del laberinto
        self.tamano_celda = 16  # Tamaño de cada celda del mapa
        self.TAMANO_PARED = 8  # Tamaño de las paredes

        # Desplazamiento del mapa en la pantalla
        self.OFFSET_X = -11  # Desplazamiento horizontal (izquierda)
        self.OFFSET_Y = -10  # Desplazamiento vertical (arriba)

    def es_pared(self, x, y):
        """
        Verifica si una posición contiene una pared.

        Args:
            x (int): Coordenada X en el mapa
            y (int): Coordenada Y en el mapa

        Returns:
            bool: True si hay una pared, False en caso contrario
        """
        if 0 <= y < self.datos.shape[0] and 0 <= x < self.datos.shape[1]:
            return self.datos[y][x] == 'X'  # 'X' representa una pared en el mapa
        return True  # Si está fuera del mapa, se considera pared

    def es_casa_fantasmas(self, x, y):
        """
        Verifica si una posición es parte de la casa de los fantasmas.

        Args:
            x (int): Coordenada X en el mapa
            y (int): Coordenada Y en el mapa

        Returns:
            bool: True si es parte de la casa de fantasmas, False en caso contrario
        """
        if 0 <= y < self.altura and 0 <= x < self.ancho:
            return self.datos[y][x] == '='  # '=' representa la casa de fantasmas
        return False

    def cargar_mapa(self, archivo):
        """
        Carga el mapa desde un archivo de texto.

        Args:
            archivo (str): Ruta del archivo que contiene el mapa
        """
        self.datos = np.loadtxt(archivo, dtype='<U1')  # Carga el mapa como matriz de caracteres
        self.altura = self.datos.shape[0]  # Número de filas
        self.ancho = self.datos.shape[1]  # Número de columnas

    def actualizar(self, dt, modo_freight=False):
        if modo_freight:
            # Maneja el parpadeo durante el modo freight
            self.tiempo_parpadeo += dt
            if self.tiempo_parpadeo >= self.intervalo_parpadeo:
                self.parpadeo_activo = not self.parpadeo_activo  # Alterna el estado del parpadeo
                self.tiempo_parpadeo = 0
        else:
            # Resetea el parpadeo cuando no está en modo freight
            self.parpadeo_activo = False
            self.tiempo_parpadeo = 0

    def color_mapa(self, nivel):
        """
        Establece el color del mapa según el nivel actual.
        """
        if nivel == 1:
            self.color = AZUL
        elif nivel == 2:
            self.color = ROJO
        elif nivel == 3:
            self.color = AMARILLO

    def tiene_pared_adyacente(self, x, y, direccion):
        """
        Verifica si hay una pared en la dirección especificada.

        Args:
            x (int): Coordenada X actual
            y (int): Coordenada Y actual
            direccion (str): Dirección a verificar ('arriba', 'abajo', 'izquierda', 'derecha')

        Returns:
            bool: True si hay una pared adyacente en esa dirección
        """
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
        """
        Dibuja el mapa en la superficie proporcionada.
        """
        # Determina el color actual basado en el estado del parpadeo
        color_actual = BLANCO if self.parpadeo_activo else self.color
        superficie.fill(NEGRO)  # Limpia la superficie con color negro

        # Dibuja las paredes del laberinto
        for y in range(self.altura):
            for x in range(self.ancho):
                if self.es_pared(x, y):
                    # Calcula la posición en píxeles con los offsets
                    px = x * ANCHOCELDA + self.OFFSET_X
                    py = y * ALTURACELDA + self.OFFSET_Y

                    # Dibuja cada borde solo si no hay una pared adyacente
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

        # Dibuja la casa de los fantasmas
        for y in range(self.altura):
            for x in range(self.ancho):
                if self.es_casa_fantasmas(x, y):
                    px = x * ANCHOCELDA * 2 + self.OFFSET_X
                    py = y * ALTURACELDA * 2 + self.OFFSET_Y
                    pygame.draw.line(superficie, BLANCO,
                                     (px, py),
                                     (px + ANCHOCELDA, py),
                                     self.grosor_linea)