import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *
from random import randint
from random import choice
class Pinky(object):
    def __init__(self,nodo):
        self.nombre = CLYDE
        self.direcciones = {STOP: Vector1(0, 0), ARRIBA: Vector1(0, -1), ABAJO: Vector1(0, 1),
                            IZQUIERDA: Vector1(-1, 0), DERECHA: Vector1(1, 0)}
        self.direccion = STOP
        self.velocidad = 85 * ANCHOCELDA / 16  # Esto es una formula que sirve para que en cualquier formato de pantalla el pacman vaya a una velocidad considerable
        self.radio = 10
        self.color = ROSADO
        self.nodo = nodo
        self.setPosicion()
        self.blanco = nodo
        self.radioColision = 5

    def setPosicion(self):
        self.posicion = self.nodo.posicion.copiar()

    def actualizar(self, pacman):
        # Actualizar la posición actual
        self.posicion += self.direcciones[self.direccion] * self.velocidad * dt

        # Verificar si llegamos al nodo objetivo
        if self.overshotTarget():
            # Establecer el nodo actual como el nodo objetivo que acabamos de alcanzar
            self.nodo = self.blanco

            # Manejar portales
            if self.nodo.vecinos[PORTAL] is not None:
                self.nodo = self.nodo.vecinos[PORTAL]

            # Elegir una nueva dirección aleatoria válida
            self.elegirDireccionAleatoria()

            # Establecer el nuevo nodo objetivo
            self.blanco = self.getNuevoBlanco(self.direccion)

            # Resetear la posición exactamente al nodo actual
            self.setPosicion()

    def elegirDireccionAleatoria(self):
        # Obtener todas las direcciones posibles desde el nodo actual
        direcciones_posibles = []
        for direccion in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]:
            # No queremos que el fantasma se dé la vuelta a menos que sea necesario
            if self.validarDireccion(direccion) and not self.direccionOpuesta(direccion):
                direcciones_posibles.append(direccion)

        # Si no hay direcciones válidas excepto la opuesta, permitir dar la vuelta
        if not direcciones_posibles and self.validarDireccion(self.direccion * -1):
            direcciones_posibles.append(self.direccion * -1)

        # Si hay direcciones posibles, elegir una al azar
        if direcciones_posibles:
            self.direccion = choice(direcciones_posibles)
        else:
            self.direccion=STOP



    def validarDireccion(self, direccion):
        if direccion is not STOP:
            if self.nodo.vecinos[direccion] is not None:
                return True
        return False

    def getNuevoBlanco(self, direccion):
        if self.validarDireccion(direccion):
            return self.nodo.vecinos[direccion]
        return self.nodo

    def overshotTarget(self):
        if self.blanco is not None:
            vec1 = self.blanco.posicion - self.nodo.posicion
            vec2 = self.posicion - self.nodo.posicion
            nodo2Blanco = vec1.magnitudCuadrada()
            nodo2Self = vec2.magnitudCuadrada()
            return nodo2Self >= nodo2Blanco
        return False

    def direccionReversa(self):
        self.direccion *= -1
        temp = self.nodo
        self.nodo = self.blanco
        self.blanco = temp

    def direccionOpuesta(self, direccion):
        if direccion is not STOP:
            if direccion == self.direccion * -1:
                return True
        return False

    def render(self, pantalla):
        p = self.posicion.entero()
        pygame.draw.circle(pantalla, self.color, p, self.radio)

    # def comer_pellets(self, lista_pellets):
    #     # Recorremos la lista de los pellets hasta encontrar uno que tenga colision con pacman
    #     # Se toma la raiz cuadrada de las distancias para evitar el uso de raices
    #
    #     for pellet in lista_pellets:
    #         distancia = self.posicion - pellet.posicion  # Vector de distancia entre pacman y el pellet
    #         distancia_potencia = distancia.magnitudCuadrada()
    #         radio_potencia = (pellet.radio + self.radioColision) ** 2
    #
    #         # Si la distancia es menor o igual al radio de los dos, significa que hay colision
    #         # Utilizando la teoria del circle to circle check para las colisiones
    #
    #         if distancia_potencia <= radio_potencia:
    #             return pellet
    #     return None