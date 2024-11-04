import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *
from Entidad import Entidad


class Pacman(Entidad):
    def __init__(self, nodo):
        super().__init__(nodo)  # Llamada al constructor de la clase padre
        self.nombre = PACMAN
        self.color = AMARILLO
        self.velocidad = 100 * ANCHOCELDA / 16  # Sobreescribe la velocidad del padre
        # Atributos específicos de Pacman
        self.direccion_deseada = STOP
        self.tiene_poder = False
        self.tiempo_poder = 0
        self.duracion_poder = 7


    def comer_pellets(self, lista_pellets):
        """Verifica colisiones con pellets."""
        for pellet in lista_pellets:
            distancia = self.posicion - pellet.posicion
            distancia_potencia = distancia.magnitudCuadrada()
            radio_potencia = (pellet.radio + self.radio_colision) ** 2
            if distancia_potencia <= radio_potencia:

                return pellet
        return None

    def actualizar(self, dt):

        # Actualizar posición actual
        self.posicion += self.direcciones[self.direccion] * self.velocidad * dt

        direccion = self.entrada_teclado()
        if direccion != STOP:
            self.direccion_deseada = direccion

        if self.blanco_sobrepasado():
            self.nodo = self.blanco

            if self.nodo.vecinos[PORTAL] is not None:
                self.nodo = self.nodo.vecinos[PORTAL]

            if self.direccion_deseada != STOP:
                if self.validar_direccion(self.direccion_deseada):
                    self.direccion = self.direccion_deseada
                    self.direccion_deseada = STOP

            self.blanco = self.get_nuevo_blanco(self.direccion)

            if self.blanco is self.nodo:
                self.direccion = STOP

            self.set_posicion()
        else:
            if self.direccion_opuesta(direccion):
                self.direccion_reversa()

    def render(self, pantalla):

        p = self.posicion.entero()
        pygame.draw.circle(pantalla, self.color, p, self.radio)
        if self.tiene_poder:
            pygame.draw.circle(pantalla, AZUL, p, self.radio + 2, 2)

    def entrada_teclado(self):

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