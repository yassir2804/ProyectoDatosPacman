#Clase encargada de manejar los vectores

import math

class Vector1(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.umbral = 0.000001

    def __add__(self, other):
        return Vector1(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector1(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        return Vector1(self.x * other, self.y * other)
    def __truediv__(self, scalar):
        if scalar != 0:
            return Vector1(self.x / float(scalar), self.y / float(scalar))
        return None
    def __eq__(self, other):
        if abs(self.x-other.x) < self.umbral:
            if abs(self.y-other.y) < self.umbral:
                return True
        return False
    def magnitudCuadrada(self):
        return self.x ** 2 + self.y ** 2
    def magnitud(self):
        return math.sqrt(self.magnitudCuadrada())
    def copiar(self):
        return Vector1(self.x, self.y)
    def tupla(self):
        return self.x, self.y
    def entero(self):
        return int(self.x), int(self.y)
    def __str__(self):
        return "<"+str(self.x) + "," + str(self.y)+">"
    def __hash__(self):
        return hash((self.x, self.y))
    def __eq__(self, other):
        if not isinstance(other, Vector1):
            return False
        return self.x == other.x and self.y == other.y