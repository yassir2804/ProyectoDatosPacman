
from Pacman import *
from numpy.random import random
from Constantes import *
from Entidad import *
from Modo import Controladora_Modos


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



class Blinky(Fantasma):
    def __init__(self, nodo,pacman=None):
        # Call parent constructor first
        super().__init__(nodo, pacman)

        # Override ghost properties
        self.nombre = BLINKY
        self.color = ROJO
        self.velocidad = 50 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

