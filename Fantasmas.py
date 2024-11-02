
from Pacman import *
from numpy.random import random
from Constantes import *

class fantasma(object):
    def __init__(self, nodo,grafo):
        self.nombre = GHOST
        self.puntos = 150
        self.direcciones = {STOP: Vector1(0, 0), ARRIBA: Vector1(0, -1), ABAJO: Vector1(0, 1),IZQUIERDA: Vector1(-1, 0),DERECHA: Vector1(1, 0)}
        self.direcciones_opuestas = {ARRIBA: ABAJO, ABAJO: ARRIBA, IZQUIERDA: DERECHA, DERECHA: IZQUIERDA, STOP: STOP}
        # Propiedades básicas
        self.direccion = STOP
        self.nodo=nodo
        self.blanco = nodo
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5
        self.grafo = grafo
        self.directionMethod = self.goalDirection
        self.blinky = blinky
        self.modo = CHASE
        self.pathfinder = PathFinder(grafo)

        # Propiedades del modo scatter
        self.tiempo_scatter = 0
        self.duracion_scatter = 7
        self.esquina_scatter = None
        self.encontrar_esquina_scatter()

        self.set_posicion()
        self.iniciar_movimiento()

    def set_posicion(self):
        """Establece la posición en el nodo actual."""
        self.posicion = self.nodo.posicion.copiar()

    def render(self, pantalla):
        """Dibuja el fantasma en la pantalla."""
        p = self.posicion.entero()
        color_actual = PURPURA if self.modo == SCATTER else self.color
        pygame.draw.circle(pantalla, color_actual, p, self.radio)

    @abstractmethod
    def calcular_objetivo(self, pacman):
        """Calcula el punto objetivo específico del fantasma"""
        pass

    @abstractmethod
    def actualizar_direccion(self, pacman):
        """Actualiza la dirección del fantasma."""
        pass

    def encontrar_esquina_scatter(self):
        """Define una esquina del mapa para el modo scatter."""
        # Se puede sobrecargar en cada fantasma para elegir esquinas diferentes
        pass


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
