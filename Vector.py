#Clase encargada de manejar los vectores

import math

class Vector1(object):
    """
        Clase encargada de manejar los vectores bidimensionales. Esta clase proporciona metodos
        para realizar operaciones comunes con vectores como la suma, resta, multiplicacion por un
        escalar, y division por un escalar. Ademas, incluye metodos para calcular la magnitud del
        vector, compararlo con otro vector, copiarlo, obtenerlo como una tupla o convertirlo a enteros.
        La clase tambien ofrece representaciones de texto del vector y permite el uso de vectores como
        claves en diccionarios al implementar un metodo de hash.
    """

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
