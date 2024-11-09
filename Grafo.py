import pygame
from Vector import Vector1
from Constantes import *
from Entidad import *
import numpy as np


class Nodo:
    """
    Representa un nodo en el grafo del laberinto.
    Mantiene información sobre sus vecinos y las entidades que pueden acceder a él.
    """

    def __init__(self, x, y):
        """
        Inicializa un nodo con su posición y conexiones.

        Args:
            x (int): Posición X en píxeles
            y (int): Posición Y en píxeles
        """
        self.posicion = Vector1(x, y)
        # Diccionario de nodos vecinos en cada dirección
        self.vecinos = {
            ARRIBA: None,
            ABAJO: None,
            IZQUIERDA: None,
            DERECHA: None,
            PORTAL: None
        }
        # Lista de entidades que pueden moverse en cada dirección
        self.acceso = {
            ARRIBA: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA],
            ABAJO: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA],
            IZQUIERDA: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA],
            DERECHA: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA]
        }

    def denegar_acceso(self, direccion, entidad):
        """Remueve el permiso de una entidad para moverse en una dirección"""
        if entidad.nombre in self.acceso[direccion]:
            self.acceso[direccion].remove(entidad.nombre)

    def dar_acceso(self, direccion, entidad):
        """Otorga permiso a una entidad para moverse en una dirección"""
        if entidad.nombre not in self.acceso[direccion]:
            self.acceso[direccion].append(entidad.nombre)


class Grafo:
    """
    Representa el laberinto completo como un grafo de nodos conectados.
    Maneja la creación, conexión y gestión de accesos del laberinto.
    """

    def __init__(self, nivel):
        """
        Inicializa el grafo a partir de un archivo de nivel.

        Args:
            nivel (str): Ruta al archivo que contiene el layout del nivel
        """
        self.nivel = nivel
        self.nodosLUT = {}  # Diccionario de búsqueda de nodos por posición
        self.casa = None  # Nodo especial para la casa de los fantasmas

        # Símbolos utilizados en el archivo de nivel
        self.simbolosNodos = ['+', 'P', 'n']  # Símbolos que representan nodos
        self.simbolosCaminos = ['.', '-', '|', 'p']  # Símbolos que representan caminos

        # Construir el grafo
        self._construir_grafo()

    def _construir_grafo(self):
        """Proceso completo de construcción del grafo"""
        datos = self.leer_laberinto(self.nivel)
        self.crear_tabla_nodos(datos)
        self.conectar_horizontal(datos)
        self.conectar_vertical(datos)

    # Métodos de construcción del grafo
    def leer_laberinto(self, archivo_texto):
        """Lee el archivo de nivel y lo convierte en una matriz"""
        return np.loadtxt(archivo_texto, dtype='<U1')

    def construir_clave(self, col, fila):
        """Convierte coordenadas de tile a píxeles para usar como clave"""
        return col * ANCHOCELDA, fila * ALTURACELDA

    def crear_tabla_nodos(self, datos, xbalance=0, ybalance=0):
        """
        Crea los nodos del grafo basados en la matriz del nivel.

        Args:
            datos: Matriz que representa el nivel
            xbalance: Desplazamiento X para la posición de los nodos
            ybalance: Desplazamiento Y para la posición de los nodos
        """
        for fila in range(datos.shape[0]):
            for col in range(datos.shape[1]):
                if datos[fila][col] in self.simbolosNodos:
                    x, y = self.construir_clave(col + xbalance, fila + ybalance)
                    self.nodosLUT[(x, y)] = Nodo(x, y)

    def conectar_horizontal(self, datos, xbalance=0, ybalance=0):
        """Conecta nodos adyacentes horizontalmente"""
        for fila in range(datos.shape[0]):
            clave = None
            for col in range(datos.shape[1]):
                if datos[fila][col] in self.simbolosNodos:
                    if clave is None:
                        clave = self.construir_clave(col + xbalance, fila + ybalance)
                    else:
                        otra_clave = self.construir_clave(col + xbalance, fila + ybalance)
                        self._conectar_nodos(clave, otra_clave, DERECHA)
                        clave = otra_clave
                elif datos[fila][col] not in self.simbolosCaminos:
                    clave = None

    def conectar_vertical(self, datos, xbalance=0, ybalance=0):
        """Conecta nodos adyacentes verticalmente"""
        datos_transpuestos = datos.transpose()
        for col in range(datos_transpuestos.shape[0]):
            clave = None
            for fila in range(datos_transpuestos.shape[1]):
                if datos_transpuestos[col][fila] in self.simbolosNodos:
                    if clave is None:
                        clave = self.construir_clave(col + xbalance, fila + ybalance)
                    else:
                        otra_clave = self.construir_clave(col + xbalance, fila + ybalance)
                        self._conectar_nodos(clave, otra_clave, ABAJO)
                        clave = otra_clave
                elif datos_transpuestos[col][fila] not in self.simbolosCaminos:
                    clave = None

    def _conectar_nodos(self, clave1, clave2, direccion):
        """Helper para conectar dos nodos en una dirección específica"""
        self.nodosLUT[clave1].vecinos[direccion] = self.nodosLUT[clave2]
        self.nodosLUT[clave2].vecinos[direccion * -1] = self.nodosLUT[clave1]

    # Métodos de acceso a nodos
    def obtener_nodo_desde_pixeles(self, pixel_x, pixel_y):
        """Obtiene un nodo dadas sus coordenadas en píxeles"""
        return self.nodosLUT.get((pixel_x, pixel_y))

    def obtener_nodo_desde_tiles(self, col, fila):
        """Obtiene un nodo dadas sus coordenadas en tiles"""
        x, y = self.construir_clave(col, fila)
        return self.nodosLUT.get((x, y))

    def obtener_nodo_temporal_inicio(self):
        """Retorna el primer nodo del grafo"""
        return list(self.nodosLUT.values())[0]

    # Métodos para portales y casa de fantasmas
    def set_portales(self, par1, par2):
        """Conecta dos nodos como portales (túneles)"""
        clave1 = self.construir_clave(*par1)
        clave2 = self.construir_clave(*par2)
        if clave1 in self.nodosLUT and clave2 in self.nodosLUT:
            self.nodosLUT[clave1].vecinos[PORTAL] = self.nodosLUT[clave2]
            self.nodosLUT[clave2].vecinos[PORTAL] = self.nodosLUT[clave1]

    def crear_nodos_casa(self, xbalance, ybalance):
        """
        Crea la estructura de nodos para la casa de los fantasmas.

        Returns:
            tuple: Coordenadas del nodo central de la casa
        """
        datos_casa = np.array([
            ['X', 'X', '+', 'X', 'X'],
            ['X', 'X', '.', 'X', 'X'],
            ['+', 'X', '.', 'X', '+'],
            ['+', '.', '+', '.', '+'],
            ['+', 'X', 'X', 'X', '+']
        ])

        self.crear_tabla_nodos(datos_casa, xbalance, ybalance)
        self.conectar_horizontal(datos_casa, xbalance, ybalance)
        self.conectar_vertical(datos_casa, xbalance, ybalance)
        self.casa = self.construir_clave(xbalance + 2, ybalance)
        return self.casa

    def conectar_nodos_casa(self, casa, otro, direccion):
        """Conecta la casa de fantasmas con el resto del laberinto"""
        clave = self.construir_clave(*otro)
        self._conectar_nodos(casa, clave, direccion)

    # Métodos de gestión de acceso
    def denegar_acceso(self, col, row, direccion, entidad):
        """Deniega acceso a una entidad en un nodo específico"""
        if nodo := self.obtener_nodo_desde_tiles(col, row):
            nodo.denegar_acceso(direccion, entidad)

    def dar_acceso(self, col, row, direccion, entidad):
        """Otorga acceso a una entidad en un nodo específico"""
        if nodo := self.obtener_nodo_desde_tiles(col, row):
            nodo.dar_acceso(direccion, entidad)

    def denegar_acceso_entidades(self, col, row, direccion, entidades):
        """Deniega acceso a múltiples entidades en un nodo"""
        for entidad in entidades:
            self.denegar_acceso(col, row, direccion, entidad)

    def dar_acceso_entidades(self, col, row, direccion, entidades):
        """Otorga acceso a múltiples entidades en un nodo"""
        for entidad in entidades:
            self.dar_acceso(col, row, direccion, entidad)

    # Métodos específicos para la casa de fantasmas
    def denegar_acceso_a_casa(self, entidad):
        """Deniega acceso a una entidad para entrar a la casa"""
        self.nodosLUT[self.casa].denegar_acceso(ABAJO, entidad)

    def dar_acceso_a_casa(self, entidad):
        """Otorga acceso a una entidad para entrar a la casa"""
        self.nodosLUT[self.casa].dar_acceso(ABAJO, entidad)

    def denegar_acceso_a_casa_entidades(self, entidades):
        """Deniega acceso a múltiples entidades para entrar a la casa"""
        for entidad in entidades:
            self.denegar_acceso_a_casa(entidad)

    def dar_acceso_a_casa_entidades(self, entidades):
        """Otorga acceso a múltiples entidades para entrar a la casa"""
        for entidad in entidades:
            self.dar_acceso_a_casa(entidad)