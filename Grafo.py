import pygame
from Vector import Vector1
from Constantes import *
from Entidad import *
import numpy as np

class Nodo(object):
    def __init__(self, x, y):
        self.posicion = Vector1(x, y)
        self.vecinos = {
            ARRIBA: None,
            ABAJO: None,
            IZQUIERDA: None,
            DERECHA: None,
            PORTAL: None
        }
        self.acceso = {ARRIBA: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA],
                       ABAJO: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA],
                       IZQUIERDA: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA],
                       DERECHA: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUTA]}

    def denegar_acceso(self, direccion, entidad):
        if entidad.nombre in self.acceso[direccion]:
            self.acceso[direccion].remove(entidad.nombre)

    def dar_acceso(self, direccion, entidad):
        if entidad.nombre not in self.acceso[direccion]:
            self.acceso[direccion].append(entidad.nombre)



class Grafo(object):
    def __init__(self, nivel):
        self.nivel = nivel
        self.nodosLUT = {}
        self.simbolosNodos = ['+', 'P', 'n']
        self.simbolosCaminos = ['.', '-', '|', 'p']
        self.casa = None
        datos = self.leer_laberinto(nivel)
        self.crear_tabla_nodos(datos)
        self.conectar_horizontal(datos)
        self.conectar_vertical(datos)

    def leer_laberinto(self, archivoTexto):
        return np.loadtxt(archivoTexto, dtype='<U1')

    def crear_tabla_nodos(self, datos, xbalance=0, ybalance=0):
        for fila in range(datos.shape[0]):
            for col in range(datos.shape[1]):
                if datos[fila][col] in self.simbolosNodos:
                    x, y = self.construir_clave(col + xbalance, fila + ybalance)
                    self.nodosLUT[(x, y)] = Nodo(x, y)
                    # Debug: muestra la posición del tile donde se crea el nodo
                    print(f"Nodo creado en tile: ({col + xbalance}, {fila + ybalance}) - Símbolo: {datos[fila][col]}")

    def construir_clave(self, col, fila):
        return col * ANCHOCELDA, fila * ALTURACELDA

    def conectar_horizontal(self, datos, xbalance=0, ybalance=0):
        for fila in range(datos.shape[0]):
            clave = None
            for col in range(datos.shape[1]):
                if datos[fila][col] in self.simbolosNodos:
                    if clave is None:
                        clave = self.construir_clave(col + xbalance, fila + ybalance)
                    else:
                        otra_clave = self.construir_clave(col + xbalance, fila + ybalance)
                        self.nodosLUT[clave].vecinos[DERECHA] = self.nodosLUT[otra_clave]
                        self.nodosLUT[otra_clave].vecinos[IZQUIERDA] = self.nodosLUT[clave]
                        clave = otra_clave
                elif datos[fila][col] not in self.simbolosCaminos:
                    clave = None

    def conectar_vertical(self, datos, xbalance=0, ybalance=0):
        datos_transpuestos = datos.transpose()
        for col in range(datos_transpuestos.shape[0]):
            clave = None
            for fila in range(datos_transpuestos.shape[1]):
                if datos_transpuestos[col][fila] in self.simbolosNodos:
                    if clave is None:
                        clave = self.construir_clave(col + xbalance, fila + ybalance)
                    else:
                        otra_clave = self.construir_clave(col + xbalance, fila + ybalance)
                        self.nodosLUT[clave].vecinos[ABAJO] = self.nodosLUT[otra_clave]
                        self.nodosLUT[otra_clave].vecinos[ARRIBA] = self.nodosLUT[clave]
                        clave = otra_clave
                elif datos_transpuestos[col][fila] not in self.simbolosCaminos:
                    clave = None

    def obtener_nodo_desde_pixeles(self, pixel_x, pixel_y):
        if (pixel_x, pixel_y) in self.nodosLUT.keys():
            return self.nodosLUT[(pixel_x, pixel_y)]
        return None

    def obtener_nodo_desde_tiles(self, col, fila):
        x, y = self.construir_clave(col, fila)
        if (x, y) in self.nodosLUT.keys():
            return self.nodosLUT[(x, y)]
        return None

    def obtener_nodo_temporal_inicio(self):
        nodos = list(self.nodosLUT.values())
        return nodos[0]

    def set_portales(self, par1, par2):
        clave1 = self.construir_clave(*par1)
        clave2 = self.construir_clave(*par2)
        if clave1 in self.nodosLUT.keys() and clave2 in self.nodosLUT.keys():
            self.nodosLUT[clave1].vecinos[PORTAL] = self.nodosLUT[clave2]
            self.nodosLUT[clave2].vecinos[PORTAL] = self.nodosLUT[clave1]

    def crear_nodos_casa(self, xbalance, ybalance):
        print("\n=== CREANDO NODOS DE LA CASA ===")
        datos_casa = np.array([['X', 'X', '+', 'X', 'X'],
                               ['X', 'X', '.', 'X', 'X'],
                               ['+', 'X', '.', 'X', '+'],
                               ['+', '.', '+', '.', '+'],
                               ['+', 'X', 'X', 'X', '+']])
        print("\nMatriz de la casa:")
        print(datos_casa)

        self.crear_tabla_nodos(datos_casa, xbalance, ybalance)
        self.conectar_horizontal(datos_casa, xbalance, ybalance)
        self.conectar_vertical(datos_casa, xbalance, ybalance)
        self.casa = self.construir_clave(xbalance + 2, ybalance)
        print(f"\nNodo casa establecido en: ({xbalance + 2}, {ybalance})")
        return self.casa

    def conectar_nodos_casa(self, casa, otro, direccion):
        clave = self.construir_clave(*otro)
        self.nodosLUT[casa].vecinos[direccion] = self.nodosLUT[clave]
        self.nodosLUT[clave].vecinos[direccion * -1] = self.nodosLUT[casa]


    def denegar_acceso(self, col, row, direccion, entidad):
        nodo = self.obtener_nodo_desde_tiles(col, row)
        if nodo is not None:
            nodo.denegar_acceso(direccion, entidad)

    def dar_acceso(self, col, row, direccion, entidad):
        nodo = self.obtener_nodo_desde_tiles(col, row)
        if nodo is not None:
            nodo.dar_acceso(direccion, entidad)

    def denegar_acceso_entidades(self, col, row, direccion, entidades):
        for entity in entidades:
            self.denegar_acceso(col, row, direccion, entity)

    def dar_acceso_entidades(self, col, row, direccion, entidades):
        for entidad in entidades:
            self.dar_acceso(col, row, direccion, entidad)

    def denegar_acceso_a_casa(self, entidad):
        self.nodosLUT[self.casa].denegar_acceso(ABAJO, entidad)

    def dar_acceso_a_casa(self, entidad):
        self.nodosLUT[self.casa].dar_acceso(ABAJO, entidad)

    def denegar_acceso_a_casa_entidades(self, entidades):
        for entidad in entidades:
            self.denegar_acceso_a_casa(entidad)

    def dar_acceso_a_casa_entidades(self, entidades):
        for entidad in entidades:
            self.dar_acceso_a_casa(entidad)