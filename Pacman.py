import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *


class Pacman(object):
    def __init__(self, nodo):
        self.nombre = PACMAN
        self.direcciones = {STOP: Vector1(0, 0), ARRIBA: Vector1(0, -1), ABAJO: Vector1(0, 1),
                            IZQUIERDA: Vector1(-1, 0), DERECHA: Vector1(1, 0)}
        self.direccion = STOP
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.color = AMARILLO
        self.nodo = nodo
        self.setPosicion()
        self.blanco = nodo
        self.radioColision = 5
        self.direccion_deseada = STOP

    def setPosicion(self):
        self.posicion = self.nodo.posicion.copiar()

    def actualizar(self, dt):
        # Actualizar posición actual
        self.posicion += self.direcciones[self.direccion] * self.velocidad * dt

        # Obtener entrada del teclado
        direccion = self.entradaTeclado()
        if direccion != STOP:
            self.direccion_deseada = direccion

        # Verificar si llegamos al nodo objetivo
        if self.overshotTarget():
            # Establecer el nodo actual como el nodo objetivo que acabamos de alcanzar
            self.nodo = self.blanco

            # Manejar portales
            if self.nodo.vecinos[PORTAL] is not None:
                self.nodo = self.nodo.vecinos[PORTAL]

            # Solo aquí, cuando llegamos a un nodo, intentamos cambiar la dirección
            if self.direccion_deseada != STOP:
                if self.validarDireccion(self.direccion_deseada):
                    self.direccion = self.direccion_deseada
                    self.direccion_deseada = STOP

            # Determinar el siguiente nodo objetivo basado en la dirección actual
            self.blanco = self.getNuevoBlanco(self.direccion)

            # Si no hay un camino válido, detenerse
            if self.blanco is self.nodo:
                self.direccion = STOP

            # Resetear la posición exactamente al nodo actual
            self.setPosicion()
        else:
            # Solo permitir cambio de dirección en medio camino si es dirección opuesta
            if self.direccionOpuesta(direccion):
                self.direccionReversa()

    def validarDireccion(self, direccion):
        if direccion is not STOP:
            if self.nodo.vecinos[direccion] is not None:
                return True
        return False

    def getNuevoBlanco(self, direccion):
        if self.validarDireccion(direccion):
            return self.nodo.vecinos[direccion]
        return self.nodo


    def entradaTeclado(self):
        teclaPresionada = pygame.key.get_pressed()
        if teclaPresionada[K_UP]:
            return ARRIBA
        if teclaPresionada[K_DOWN]:
            return ABAJO
        if teclaPresionada[K_LEFT]:
            return IZQUIERDA
        if teclaPresionada[K_RIGHT]:
            return DERECHA
        return STOP

    def overshotTarget(self):
        if self.blanco is not None:
            vec1 = self.blanco.posicion- self.nodo.posicion
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

    def comer_pellets(self,lista_pellets):
        #Recorremos la lista de los pellets hasta encontrar uno que tenga colision con pacman
        #Se toma la raiz cuadrada de las distancias para evitar el uso de raices

        for pellet in lista_pellets:
            distancia = self.posicion - pellet.posicion #Vector de distancia entre pacman y el pellet
            distancia_potencia = distancia.magnitudCuadrada()
            radio_potencia = (pellet.radio + self.radioColision) ** 2

            #Si la distancia es menor o igual al radio de los dos, significa que hay colision
            #Utilizando la teoria del circle to circle check para las colisiones

            if distancia_potencia <= radio_potencia:
                return pellet
        return None