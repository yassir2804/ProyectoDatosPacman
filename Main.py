import pygame
from pygame.locals import *
from Constantes import *
from Grafo import Grafo
from Pacman import Pacman
from Pellet import GrupoPellets
from Clyde import Clyde
from Blinky import Blinky
from Pinky import Pinky
from Inky import Inky
from Texto import GrupoTexto


class Controladora(object):
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMANIOPANTALLA, 0, 32)
        self.fondo = None
        self.clock = pygame.time.Clock()
        self.grafo = Grafo("mazetest.txt")
        self.grafo.set_portales((0, 17), (27, 17))

        # Crear los fantasmas primero
        self.Clyde = Clyde(self.grafo.punto_partida_fantasmas(), self.grafo)
        self.Blinky = Blinky(self.grafo.punto_partida_fantasmas(), self.grafo)
        self.Pinky = Pinky(self.grafo.punto_partida_fantasmas(), self.grafo)
        self.Inky = Inky(self.grafo.punto_partida_fantasmas(), self.grafo)

        # Crear Pacman y establecer los fantasmas
        self.pacman = Pacman(self.grafo.punto_partida_pacman())
        self.lista_fantasmas = [self.Blinky]
        self.pacman.establecerFantasmas(self.lista_fantasmas)

        self.Pellet = GrupoPellets("mazetest.txt")
        self.grupo_texto = GrupoTexto()
        self.puntaje = 0

    def verificacion_pellets(self):
        pellet = self.pacman.comer_pellets(self.Pellet.listaPellets)
        if pellet:
            self.Pellet.numComidos += 1
            if pellet.nombre == PELLETPODER:
                self.puntaje += 50  # Más puntos por power pellet
            else:
                self.puntaje += 10  # Puntos normales por pellet regular
            self.grupo_texto.actualizarPuntaje(self.puntaje)
            self.Pellet.listaPellets.remove(pellet)

    def actualizar(self):
        dt = self.clock.tick(30) / 1000
        self.pacman.actualizar(dt)
        self.Clyde.actualizar(dt)
        self.Blinky.actualizar(dt, self.pacman)
        self.Pinky.actualizar(dt, self.pacman)
        self.Inky.actualizar(dt, self.pacman, self.Blinky)
        self.Pellet.actualizar(dt)
        self.grupo_texto.actualizar(dt)
        self.verificacion_pellets()
        self.verificarEventos()
        self.render()


    def setFondo(self):
        self.fondo = pygame.surface.Surface(TAMANIOPANTALLA).convert()
        self.fondo.fill(NEGRO)

    def empezar(self):
        self.setFondo()

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
        self.Inky.render(self.pantalla)
        self.grupo_texto.renderizar(self.pantalla)
        pygame.display.update()




if __name__ == '__main__':
    juego = Controladora()
    juego.empezar()
    while True:
        juego.actualizar()