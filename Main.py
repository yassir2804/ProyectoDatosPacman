import pygame
from pygame.locals import *
from Constantes import *
from Pacman import *

class Controladora(object):
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMANIOPANTALLA, 0, 32)
        self.fondo = None
        self.clock = pygame.time.Clock()
        self.pacman = Pacman()

    def setFondo(self ):
        self.fondo = pygame.surface.Surface(TAMANIOPANTALLA).convert()
        self.fondo.fill(NEGRO)

    def empezar(self):
        self.setFondo()

    def actualizar(self):
        dt= self.clock.tick(30)/1000
        self.pacman.actualizar(dt)
        self.verificarEventos()
        self.render()

    def verificarEventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.pacman.render(self.pantalla)
        pygame.display.update()


if __name__ == '__main__':
    juego = Controladora()
    juego.empezar()
    while True:
        juego.actualizar()