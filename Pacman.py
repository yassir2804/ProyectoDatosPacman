import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *
class Pacman(object):
    def __init__(self,nodo):
        self.nombre = PACMAN
        self.direcciones = {STOP: Vector1(0,0), ARRIBA: Vector1(0,-1), ABAJO: Vector1(0,1), IZQUIERDA: Vector1(-1,0), DERECHA: Vector1(1,0)}
        self.direccion = STOP
        self.velocidad = 100* ANCHOCELDA/16 #Esto es una formula que sirve para que en cualquier formato de pantalla el pacman vaya a una velocidad considerable
        self.radio = 10
        self.color = AMARILLO
        self.nodo= nodo
        self.setPosicion()
        self.blanco=nodo
        
        
    def setPosicion(self):
        self.posicion = self.nodo.posicion.copiar()

    def actualizar(self, dt):
        self.posicion += self.direcciones[self.direccion]*self.velocidad * dt
        direc = self.entradaTeclado()
        #self.nodo= self.getNuevoBlanco(self.direccion)
        #self.setPosicion()
        if self.overshotTarget():
            self.nodo = self.blanco
            self.blanco = self.getNuevoBlanco(self.direccion)
            if self.blanco is not self.nodo:
                self.direccion =  direc
            else:
                self.blanco = self.getNuevoBlanco(direc)

            if self.blanco is self.nodo:
                self.direccion = STOP
            self.setPosicion()
        else:
            if self.direccionOpuesta(self.direccion):
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
            TOLERANCIA = 0.0001
            return nodo2Self >= nodo2Blanco - TOLERANCIA
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