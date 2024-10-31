
import pygame
from pygame.locals import *
from Constantes import *
from Grafo import *
from Pacman import *
from Grafo import Grafo
from Pellet import GrupoPellets
from Clyde import *
from Blinky import *
from Pinky import *
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
        self.Clyde = Clyde(self.grafo.punto_partida_fantasmas())
        self.Blinky = Blinky(self.grafo.punto_partida_fantasmas(), self.grafo)
        self.Pinky = Pinky(self.grafo.punto_partida_fantasmas(), self.grafo)


    def setFondo(self ):
        self.fondo = pygame.surface.Surface(TAMANIOPANTALLA).convert()
        self.fondo.fill(NEGRO)


    def empezar(self):
        self.setFondo()
        self.debug_nodos()

    def verificacion_pellets(self):
        pellet = self.pacman.comer_pellets(self.Pellet.listaPellets)
        if pellet:
            self.Pellet.numComidos += 1
            self.Pellet.listaPellets.remove(pellet)


    def actualizar(self):
        dt = self.clock.tick(30) / 1000
        self.pacman.actualizar(dt)
        self.Clyde.actualizar(dt)
        self.Blinky.actualizar(dt,self.pacman)
        self.Pinky.actualizar(dt,self.pacman)
        self.Pellet.actualizar(dt)
        self.verificacion_pellets()
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
        self.Clyde.render(self.pantalla)
        self.Blinky.render(self.pantalla)
        self.Pinky.render(self.pantalla)
        pygame.display.update()

    def debug_nodos(self):
        print("Verificación de conexiones entre nodos:")
        for nodo in self.grafo.nodosLUT.values():
            print(f"Nodo en posición: {nodo.posicion}")
            for direccion, vecino in nodo.vecinos.items():
                if vecino is not None:
                    print(f"  Vecino en dirección {direccion}: {vecino.posicion}")
                else:
                    print(f"  Sin vecino en dirección {direccion}")


if __name__ == '__main__':
    juego = Controladora()
    juego.empezar()
    while True:
        juego.actualizar()