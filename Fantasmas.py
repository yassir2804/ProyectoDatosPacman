
from Pacman import *
from numpy.random import random
from Constantes import *

class fantasma(object):
    def __init__(self, nodo, Pacman=None, blinky=None):
        Entity.__init__(self, nodo)
        self.nombre = GHOST
        self.puntos = 150
        self.objetivo = random()
        self.directionMethod = self.goalDirection
        self.pacman = Pacman
        self.modo = ModoController(self)
        self.blinky = blinky
        self.NodoCasa = nodo

    def resetear(self):
        self.puntos +=50
        self.directionMethod = self.goalDirection

    def actualizar(self, posicion):
        self.objetivo=posicion

    def cambiar_modo(self,modo):


    def scatter(self):
        self.objetivo = Vector2()

    def chase(self):
        self.objetivo = self.pacman.position

    def frihtened(self):
        self.objetivo= 0

    def spawn(self):
        self.objetivo = self.NodoCasa.position

    def setNodoDeSpawn(self, nodo):
        self.NodoCasa = node

    def startSpawn(self):
        self.modo.setSpawnMode()
        if self.modo.current == SPAWN:
            self.setVelocidad(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def startFreight(self):
        self.modo.setFreightMode()
        if self.modo.current == FREIGHT:
            self.setVelocidad(50)
            self.directionMethod = self.randomDirection

    def modoNormal(self):
        self.setVelocidad(100)
        self.directionMethod = self.goalDirection

class Blinky(fantasma):
    def __init__(self, nodo,pacman=None, blinky=None):
        fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre=Blinky
        self.color= Red

    def actualizar(self, dt):
        self.modo.update(dt)
        if self.modo.current is SCATTER:
            self.scatter()
        elif self.modo.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.objetivo= 0

    def chase(self):
        self.objetivo= 0

    def frihtened(self):
        self.objetivo= 0



class Pinky(fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre = Blinky
        self.color = ROSADO

    def actualizar(self, dt):
        self.modo.update(dt)
        if self.modo.current is SCATTER:
            self.scatter()
        elif self.modo.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.objetivo = 0

    def chase(self):
        self.objetivo = 0

    def frihtened(self):
        self.objetivo= 0

class Inky(fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre = Inky
        self.color = Teal

    def actualizar(self, dt):
        self.modo.update(dt)
        if self.modo.current is SCATTER:
            self.scatter()
        elif self.modo.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.objetivo = 0

    def chase(self):
        self.objetivo = 0

    def frihtened(self):
        self.objetivo= 0

class Clyde(fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre = Clyde
        self.color = Orange

    def actualizar(self, dt):
        self.modo.update(dt)
        if self.modo.current is SCATTER:
            self.scatter()
        elif self.modo.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.objetivo = 0

    def chase(self):
        self.objetivo = 0

    def frihtened(self):
        self.objetivo= 0


class GrupoFantasma(Object):
    def __init__(self,nodo,pacman):
        self.blinky = Blinky(nodo,pacman)
        self.Pinky = Pinky(nodo,pacman)
        self.Inky = Inky(nodo,pacman)
        self.Clyde = Clyde(nodo,pacman)
        self.fantasma = [self.blinky,self.Pinky,self.Inky,self.Clyde]

    def __iter__(self):
        return iter(self.ghosts)

    def actualizar(self, dt):
        for fantasma in self:
            fantasma.actualizar(dt)

    def startFreight(self):
        for fantasma in self:
            fantasma.startFreight()
        self.resetearPuntos()

    def setSpawnNodo(self, node):
        for fantasma in self:
            fantasma.setSpawnNodo(node)

    def actualizarPuntos(self):
        for fantasma in self:
            fantasma.puntos *= 2

    def resetearPuntos(self):
        for fantasma in self:
            fantasma.puntos = 200

    def resetear(self):
        for fantasma in self:
            fantasma.resetear()

    def hide(self):
        for fantasma in self:
            fantasma.visible = False

    def mostrar(self):
        for fantasma in self:
            fantasma.visible = True

    def render(self, screen):
        for fantasma in self:
            fantasma.render(screen)
