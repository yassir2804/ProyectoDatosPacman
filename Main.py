
import pygame
from pygame.locals import *
from Constantes import *
from Grafo import *
from Pacman import *
from Grafo import Grafo
from Pellet import GrupoPellets

class Controladora(object):
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMANIOPANTALLA, 0, 32)
        self.fondo = None
        self.clock = pygame.time.Clock()
        self.grafo = Grafo("mazetest.txt")
        self.grafo.set_portales ((0, 17), (27, 17))
        self.pacman= Pacman(self.grafo.punto_partida_pacman())
        self.Pellet = GrupoPellets("mazetest.txt")


    def setFondo(self ):
        self.fondo = pygame.surface.Surface(TAMANIOPANTALLA).convert()
        self.fondo.fill(NEGRO)


    def empezar(self):
        self.setFondo()


    def actualizar(self):
        dt = self.clock.tick(30) / 1000
        self.pacman.actualizar(dt)
        self.Pellet.actualizar(dt)
        self.verificarEventos()
        self.render()


    def verificarEventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()


    def render(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.grafo.render(self.pantalla)
        self.Pellet.render(self.pantalla)
        self.pacman.render(self.pantalla)
        pygame.display.update()


if __name__ == '__main__':
    juego = Controladora()
    juego.empezar()
    while True:
        juego.actualizar()