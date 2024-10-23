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
            ABAJO: None
        }

    def render(self, pantalla):
        for n in self.vecinos.keys():
            if self.vecinos[n] is not None:
                pygame.draw.line(pantalla, BLANCO,self.posicion.tupla(), self.vecinos[n].posicion.tupla())
                pygame.draw.circle(pantalla,ROJO,self.posicion.entero(),12)\

    def agregar_vecino(self, direccion, nodo_vecino):
        self.vecinos[direccion] = nodo_vecino


class Grafo(object):
    def __init__(self):
        self.nodos = {}  # {Vector1: Nodo}

    def setup_nodos_prueba(self):
        # Crear nodos
        nodoA = Nodo(Vector1(80, 80))
        nodoB = Nodo(Vector1(160, 80))
        nodoC = Nodo(Vector1(80, 160))
        nodoD = Nodo(Vector1(160, 160))
        nodoE = Nodo(Vector1(208, 160))
        nodoF = Nodo(Vector1(80, 320))
        nodoG = Nodo(Vector1(208, 320))

        # Establecer vecinos
        nodoA.vecinos[DERECHA] = nodoB
        nodoA.vecinos[ABAJO] = nodoC

        nodoB.vecinos[IZQUIERDA] = nodoA
        nodoB.vecinos[ABAJO] = nodoD

        nodoC.vecinos[ARRIBA] = nodoA
        nodoC.vecinos[DERECHA] = nodoD
        nodoC.vecinos[ABAJO] = nodoF

        nodoD.vecinos[ARRIBA] = nodoB
        nodoD.vecinos[IZQUIERDA] = nodoC
        nodoD.vecinos[DERECHA] = nodoE

        nodoE.vecinos[IZQUIERDA] = nodoD
        nodoE.vecinos[ABAJO] = nodoG

        nodoF.vecinos[ARRIBA] = nodoC
        nodoF.vecinos[DERECHA] = nodoG

        nodoG.vecinos[ARRIBA] = nodoE
        nodoG.vecinos[IZQUIERDA] = nodoF

        # Agregar nodos al grafo
        for nodo in [nodoA, nodoB, nodoC, nodoD, nodoE, nodoF, nodoG]:
            self.agregar_nodo(nodo)

    def render(self, pantalla):
        for nodo in self.nodos.values():
            nodo.render(pantalla)

    def agregar_nodo(self, nodo):
        self.nodos[nodo.posicion] = nodo