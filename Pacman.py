import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *
class Pacman(object):
    def __init__(self):
        self.nombre = PACMAN
        self.posicion = Vector1(200, 400)
        self.direcciones = {STOP: Vector1(0,0), ARRIBA: Vector1(0,-1), ABAJO: Vector1(0,1), IZQUIERDA: Vector1(-1,0), DERECHA: Vector1(1,0)}
        self.direccion = STOP
        self.velocidad = 100* ANCHOCELDA/16 #Esto es una formula que sirve para que en cualquier formato de pantalla el pacman vaya a una velocidad considerable
        self.radio = 10
        self.color = AMARILLO
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
    def actualizar(self, dt):
        self.posicion += self.direcciones[self.direccion]*self.velocidad * dt
        self.direccion = self.entradaTeclado()
    def render(self, pantalla):
        p = self.posicion.entero()
        pygame.draw.circle(pantalla, self.color, p, self.radio)