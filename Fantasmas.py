
from Pacman import *
from numpy.random import random
from Constantes import *
from Entidad import *
from Modo import Controladora_Modos
from Grafo import *

class Fantasma(Entidad):
    def __init__(self, nodo,pacman=None):
        super().__init__(nodo)
        self.nombre = FANTASMA
        self.puntos = 200
        self.meta = Vector1(0,0)
        self.pacman=pacman
        self.modo= Controladora_Modos(self)

    def actualizar(self, dt):
        self.modo.actualizar(dt)
        if self.modo.current is SCATTER:
            self.scatter()
        elif self.modo.current is CHASE:
            self.chase()
        Entidad.actualizar(self, dt)


    def chase(self):
        self.meta = self.pacman.posicion

    def scatter(self):
        self.meta =Vector1(0,0)

    def modo_normal(self):
        self.set_velocidad(100)
        self.metodoDireccion =self.direccion_meta

    def modo_Freight(self):
        self.modo.modo_freight()
        if self.modo.current == FREIGHT:
            self.set_velocidad(60)
            self.metodoDireccion = self.direccion_aleatoria
    
    def modo_Chase(self):
        self.modo.modo_chase()
        if self.modo.current == CHASE:
            self.scatter()


class Blinky(Fantasma):
    def __init__(self, nodo,pacman=None):
        # Call parent constructor first
        super().__init__(nodo, pacman)

        # Override ghost properties
        self.nombre = BLINKY
        self.color = ROJO
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(0,0)

    def chase(self):
        self.meta = self.pacman.posicion

class Inky(Fantasma):
    def __init__(self, nodo,pacman=None):
        # Call parent constructor first
        super().__init__(nodo, pacman)

        # Override ghost properties
        self.nombre =INKY
        self.color = CELESTE
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(ANCHOCELDA*COLUMNAS,FILAS*ALTURACELDA)

    def chase(self):
        self.meta = self.pacman.posicion

class Clyde(Fantasma):
    def __init__(self, nodo,pacman=None):
        # Call parent constructor first
        super().__init__(nodo, pacman)

        # Override ghost properties
        self.nombre =CLYDE
        self.color = NARANJA
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(0,ANCHOCELDA*COLUMNAS)

    def chase(self):
        self.meta = self.pacman.posicion

class Pinky(Fantasma):
    def __init__(self, nodo,pacman=None):
        # Call parent constructor first
        super().__init__(nodo, pacman)

        # Override ghost properties
        self.nombre =PINKY
        self.color = ROSADO
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(ANCHOCELDA*COLUMNAS,0)

    def chase(self):
        self.meta = self.pacman.posicion

class GrupoFantasmas(object):
    def __init__(self,nodo,pacman):
        self.blinky = Blinky(nodo, pacman)
        self.pinky = Pinky(nodo, pacman)
        self.inky = Inky(nodo, pacman)
        self.clyde = Clyde(nodo, pacman)
        self.fantasmas = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.fantasmas)

    def actualizar(self, dt):
        for fantasmas in self:
            fantasmas.actualizar(dt)

    def scatter(self):
        for fantasmas in self:
            fantasmas.scatter()
    def modo_Freight(self):
        for fantasmas in self:
            fantasmas.modo_Freight()
        self.resetearPuntos()
        
    def modo_Chase(self):
        for fantasmas in self:
            fantasmas.modo_Chase()
            fantasmas.modo_normal()

    def setSpawnNode(self, node):
        for fantasmas in self:
            fantasmas.setSpawnNode(node)

    def actualizarPuntos(self):
        for fantasmas in self:
            fantasmas.puntos *= 2

    def resetearPuntos(self):
        for fantasmas in self:
            fantasmas.puntos = 200

    def reset(self):
        for fantasmas in self:
            fantasmas.reset()

    def esconder(self):
        for fantasmas in self:
            fantasmas.visible = False

    def show(self):
        for fantasmas in self:
            fantasmas.visible = True

    def render(self, screen):
        for fantasmas in self:
            fantasmas.render(screen)

