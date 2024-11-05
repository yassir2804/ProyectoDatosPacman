import pygame
from pygame.locals import *
from Constantes import *
from Grafo import Grafo
from Pacman import Pacman
from Pellet import GrupoPellets
from Texto import GrupoTexto
from Fantasmas import GrupoFantasmas

class Controladora(object):
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMANIOPANTALLA, 0, 32)
        self.fondo = None
        self.clock = pygame.time.Clock()
        self.grafo = Grafo("mazetest.txt")
        self.grafo.set_portales((0, 17), (27, 17))

        # Crear Pacman primero
        self.pacman = Pacman(self.grafo.punto_partida_pacman())

        # Crear Blinky pasando el nodo inicial, grafo y pacman
        self.fantasmas=  GrupoFantasmas(nodo=self.grafo.obtener_nodo_desde_tiles(13, 16),pacman=self.pacman)
        self.fantasmas.blinky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(16, 16))
        self.fantasmas.clyde.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(16, 20))
        self.fantasmas.inky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(18, 16))
        self.fantasmas.pinky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(14, 16))

        self.Pellet = GrupoPellets("mazetest.txt")
        self.grupo_texto = GrupoTexto()
        self.puntaje = 0
        self.tiempo_poder = 0
        self.duracion_poder = 7  # duración en segundos del modo scatter

    def verificacion_pellets(self):
        pellet = self.pacman.comer_pellets(self.Pellet.listaPellets)
        if pellet:
            self.Pellet.numComidos += 1
            if pellet.nombre == PELLETPODER:
                self.puntaje += 50  # Más puntos por power pellet
                self.fantasmas.modo_Freight()
                self.tiempo_poder = self.duracion_poder
            else:
                self.puntaje += 10  # Puntos normales por pellet regular
            self.grupo_texto.actualizarPuntaje(self.puntaje)
            self.Pellet.listaPellets.remove(pellet)

    def actualizar(self):
        dt = self.clock.tick(30) / 1000

        # Actualizar tiempo del poder
        if self.tiempo_poder > 0:
            self.tiempo_poder -= dt
            if self.tiempo_poder <= 0:
                # Cuando se acaba el tiempo, volver a modo chase
                self.fantasmas.modo_Chase()

        self.pacman.actualizar(dt)
        self.fantasmas.actualizar(dt)
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
        self.fantasmas.render(self.pantalla)
        # self.Clyde.render(self.pantalla)
        # self.Blinky.render(self.pantalla)
        # self.Pinky.render(self.pantalla)
        # self.Inky.render(self.pantalla)
        self.grupo_texto.renderizar(self.pantalla)
        pygame.display.update()


if __name__ == '__main__':
    juego = Controladora()
    juego.empezar()
    while True:
        juego.actualizar()
