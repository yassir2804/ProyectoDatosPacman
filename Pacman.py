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
        # Nuevos atributos para el poder
        self.tiene_poder = False
        self.tiempo_poder = 0
        self.duracion_poder = 7
        self.fantasmas = []

    def establecerFantasmas(self, fantasmas):
        self.fantasmas = fantasmas

    def activarPoder(self):
        self.tiene_poder = True
        self.tiempo_poder = self.duracion_poder
        for fantasma in self.fantasmas:
            fantasma.set_scatter_mode()


    def actualizarPoder(self, dt):
        if self.tiene_poder:
            self.tiempo_poder -= dt
            if self.tiempo_poder <= 0:
                self.tiene_poder = False
                self.tiempo_poder = 0
                # Cambiar los fantasmas de nuevo a modo chase
                for fantasma in self.fantasmas:
                    fantasma.modo = CHASE

    def comer_pellets(self, lista_pellets):
        for pellet in lista_pellets:
            distancia = self.posicion - pellet.posicion
            distancia_potencia = distancia.magnitudCuadrada()
            radio_potencia = (pellet.radio + self.radioColision) ** 2

            if distancia_potencia <= radio_potencia:
                if pellet.nombre == PELLETPODER:
                    self.activarPoder()
                return pellet
        return None

    def actualizar(self, dt):
        # Actualizar el estado del poder
        self.actualizarPoder(dt)

        # Actualizar posición actual
        self.posicion += self.direcciones[self.direccion] * self.velocidad * dt

        direccion = self.entradaTeclado()
        if direccion != STOP:
            self.direccion_deseada = direccion

        if self.overshotTarget():
            self.nodo = self.blanco

            if self.nodo.vecinos[PORTAL] is not None:
                self.nodo = self.nodo.vecinos[PORTAL]

            if self.direccion_deseada != STOP:
                if self.validarDireccion(self.direccion_deseada):
                    self.direccion = self.direccion_deseada
                    self.direccion_deseada = STOP

            self.blanco = self.getNuevoBlanco(self.direccion)

            if self.blanco is self.nodo:
                self.direccion = STOP

            self.setPosicion()
        else:
            if self.direccionOpuesta(direccion):
                self.direccionReversa()

    def render(self, pantalla):
        p = self.posicion.entero()
        pygame.draw.circle(pantalla, self.color, p, self.radio)
        # Efecto visual cuando tiene poder
        if self.tiene_poder:
            pygame.draw.circle(pantalla, AZUL, p, self.radio + 2, 2)

    # Mantener los métodos originales sin cambios
    def setPosicion(self):
        self.posicion = self.nodo.posicion.copiar()

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