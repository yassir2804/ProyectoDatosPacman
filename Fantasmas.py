
from Pacman import *
from numpy.random import random
from Constantes import *
from Entidad import *

class Fantasma(Entidad):
    def __init__(self, nodo):
        Entidad.__init__(self, nodo)
        self.nombre = FANTASMA
        self.puntos = 200
        self.meta = Vector1(0,0)
        self.metodoDireccion = self.direccion_meta
