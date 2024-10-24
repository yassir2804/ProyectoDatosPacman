import pygame
import sys
import os
from pygame.locals import *
from constants import *

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def empezarJuego(self):
        self.setBackground()
        self.nodos = Grafo("mazetest.txt")
        self.pacman = Pacman(self.nodos.punto_partida_pacman())

    def update(self):
        self.checkEvents()
        self.render()

    def chequearEventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()