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
        # Atributos para A*
        self.costo_g = float('inf')  # Costo desde el inicio
        self.costo_h = 0  # Costo heurístico al objetivo
        self.costo_f = float('inf')  # Costo total (g + h)
        self.padre = None  # Nodo padre para reconstruir el camino

    def reiniciar_datos_camino(self):
        """Reinicia los datos de búsqueda de camino"""
        self.costo_g = float('inf')
        self.costo_h = 0
        self.costo_f = float('inf')
        self.padre = None

    def calcular_distancia_hasta(self, otro_nodo):
        """Calcula la distancia Manhattan entre este nodo y otro"""
        return abs(self.posicion.x - otro_nodo.posicion.x) + \
            abs(self.posicion.y - otro_nodo.posicion.y)

    def obtener_vecinos_validos(self):
        """Retorna lista de vecinos válidos"""
        return [(dir, vecino) for dir, vecino in self.vecinos.items()
                if vecino is not None]

    def render(self, pantalla):
        for n in self.vecinos.keys():
            if self.vecinos[n] is not None:
                pygame.draw.line(pantalla, BLANCO, self.posicion.tupla(),
                                 self.vecinos[n].posicion.tupla())
        pygame.draw.circle(pantalla, AZUL, self.posicion.entero(), 12)

    def agregar_vecino(self, direccion, nodo_vecino):
        self.vecinos[direccion] = nodo_vecino

    def encontrar_camino_hasta(self, nodo_objetivo):
        """Encuentra el camino hasta el nodo objetivo usando A*"""
        # Reinicia todos los nodos
        self.reiniciar_datos_camino()

        # Inicializa el nodo inicial
        self.costo_g = 0
        self.costo_h = self.calcular_distancia_hasta(nodo_objetivo)
        self.costo_f = self.costo_g + self.costo_h

        nodos_abiertos = {self}  # Nodos por explorar
        nodos_cerrados = set()  # Nodos ya explorados

        while nodos_abiertos:
            # Obtiene el nodo con menor costo_f
            actual = min(nodos_abiertos, key=lambda x: (x.costo_f, x.costo_h))

            if actual == nodo_objetivo:
                # Reconstruye y retorna el camino
                camino = []
                while actual != self:
                    camino.append(actual)
                    actual = actual.padre
                return camino[::-1]

            nodos_abiertos.remove(actual)
            nodos_cerrados.add(actual)

            # Explora los vecinos
            for direccion, vecino in actual.obtener_vecinos_validos():
                if vecino in nodos_cerrados:
                    continue

                # Calcula el nuevo costo g
                costo_tentativo = actual.costo_g + 1

                if vecino not in nodos_abiertos:
                    nodos_abiertos.add(vecino)
                elif costo_tentativo >= vecino.costo_g:
                    continue

                # Este camino es el mejor hasta ahora
                vecino.padre = actual
                vecino.costo_g = costo_tentativo
                vecino.costo_h = vecino.calcular_distancia_hasta(nodo_objetivo)
                vecino.costo_f = vecino.costo_g + vecino.costo_h

        return None  # No se encontró camino

    def obtener_siguiente_direccion_hacia(self, nodo_objetivo):
        """Obtiene la siguiente dirección hacia el objetivo"""
        camino = self.encontrar_camino_hasta(nodo_objetivo)
        if not camino or not camino[0]:
            return None

        # Encuentra qué dirección lleva al siguiente nodo
        siguiente_nodo = camino[0]
        for direccion, vecino in self.obtener_vecinos_validos():
            if vecino == siguiente_nodo:
                return direccion

        return None

class Grafo(object):
    def __init__(self, nivel):
        self.nodosLUT = {}
        self.simbolosNodos = ['+', 'P', 'n']
        self.simbolosCaminos = ['.', '-', '|', 'p']
        datos = self.leer_laberinto(nivel)
        self.crear_tabla_nodos(datos)
        self.conectar_horizontal(datos)
        self.conectar_vertical(datos)

    def render(self, pantalla):
        for nodo in self.nodosLUT.values():
            nodo.render(pantalla)

    def leer_laberinto(self, archivoTexto):
        datos = np.loadtxt(archivoTexto, dtype='<U1')
        print("Datos del laberinto:")
        print(datos)
        return datos


    def crear_tabla_nodos(self, datos, xbalance=0, ybalance=0):
        for fila in range(datos.shape[0]):
            for col in range(datos.shape[1]):
                if datos[fila][col] in self.simbolosNodos:
                    x, y = self.construir_clave(col + xbalance, fila + ybalance)
                    self.nodosLUT[(x, y)] = Nodo(Vector1(x, y))
                    print(f"Nodo creado en: {(x, y)}")

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

    def punto_partida_fantasmas(self):
        # Especifica las coordenadas del nodo donde quieres que aparezca el fantasma
        col = 2  # Cambia esto por la columna deseada
        fila = 3  # Cambia esto por la fila deseada

        nodo_partida = self.obtener_nodo_desde_tiles(col, fila)
        return nodo_partida if nodo_partida else next(iter(self.nodosLUT.values()), None)

    def set_portales(self, par1, par2):
        clave1 = self.construir_clave(*par1)  # Corrección del nombre
        clave2 = self.construir_clave(*par2)  # Corrección del nombre
        if clave1 in self.nodosLUT.keys() and clave2 in self.nodosLUT.keys():  # Corrección de variable
            self.nodosLUT[clave1].vecinos[PORTAL] = self.nodosLUT[clave2]  # Asignación correcta
            self.nodosLUT[clave2].vecinos[PORTAL] = self.nodosLUT[clave1]  # Asignación correcta
