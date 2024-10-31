import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *

class Blinky:
    def __init__(self, nodo):
        self.nombre = BLINKY
        self.direcciones = {
            STOP: Vector1(0, 0),
            ARRIBA: Vector1(0, -1),
            ABAJO: Vector1(0, 1),
            IZQUIERDA: Vector1(-1, 0),
            DERECHA: Vector1(1, 0)
        }
        self.direcciones_opuestas = {
            ARRIBA: ABAJO,
            ABAJO: ARRIBA,
            IZQUIERDA: DERECHA,
            DERECHA: IZQUIERDA,
            STOP: STOP
        }

        self.direccion = STOP
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.color = ROJO
        self.nodo = nodo
        self.set_posicion()
        self.blanco = nodo
        self.radio_colision = 5

        self.iniciar_movimiento()

    def iniciar_movimiento(self):
        """Inicia el movimiento del fantasma."""
        direcciones_disponibles = self.obtener_direcciones_validas()
        if direcciones_disponibles:
            self.direccion = direcciones_disponibles[0]
            self.blanco = self.nodo.vecinos[self.direccion]

    def actualizar(self, dt, pacman):
        """Actualiza la posición del fantasma."""
        if self.direccion == STOP:
            self.iniciar_movimiento()
            return

        # Comprobar que Pacman tiene un nodo válido
        if pacman.nodo is None:
            return

        # Calcular movimiento hacia Pacman
        vector_movimiento = self.direcciones[self.direccion] * self.velocidad * dt
        nueva_posicion = self.posicion + vector_movimiento

        # Mantener el fantasma en la línea entre nodos
        if self.direccion in [IZQUIERDA, DERECHA]:
            nueva_posicion.y = self.nodo.posicion.y
        else:
            nueva_posicion.x = self.nodo.posicion.x

        self.posicion = nueva_posicion

        if self.overshot_target():
            self.llegar_a_nodo(pacman)

    def llegar_a_nodo(self, pacman):
        """Maneja la llegada a un nodo objetivo."""
        self.nodo = self.blanco
        self.posicion = self.nodo.posicion.copiar()

        # Manejar portales
        if self.nodo.vecinos.get(PORTAL):  # Usar get para evitar KeyError
            self.nodo = self.nodo.vecinos[PORTAL]
            self.set_posicion()

        # Actualiza dirección hacia Pacman
        self.actualizar_direccion(pacman)

    def actualizar_direccion(self, pacman):
        """Actualiza la dirección hacia Pacman."""
        direcciones_validas = self.obtener_direcciones_validas()
        mejor_direccion = None
        menor_distancia = float('inf')

        for direccion in direcciones_validas:
            nodo_siguiente = self.nodo.vecinos[direccion]
            if nodo_siguiente is None:  # Asegúrate de que el vecino no sea None
                continue

            distancia = self.distancia_a_punto(nodo_siguiente.posicion, pacman.posicion)
            if distancia < menor_distancia:
                menor_distancia = distancia
                mejor_direccion = direccion

        if mejor_direccion is not None:
            self.direccion = mejor_direccion
            self.blanco = self.nodo.vecinos[mejor_direccion]
        elif direcciones_validas:
            self.direccion = direcciones_validas[0]
            self.blanco = self.nodo.vecinos[self.direccion]

    def distancia_a_punto(self, pos1, pos2):
        """Calcula la distancia euclidiana entre dos puntos utilizando la clase Vector1."""
        return (pos1 - pos2).magnitud()

    def obtener_direcciones_validas(self):
        """Obtiene todas las direcciones válidas disponibles sin recursión."""
        return [direccion for direccion in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]
                if self.nodo.vecinos.get(direccion) is not None and  # Verifica que no sea None
                (self.direccion == STOP or direccion != self.direcciones_opuestas[self.direccion] or
                len([d for d in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]
                     if self.nodo.vecinos.get(d)]) == 1)]

    def overshot_target(self):
        """Verifica si se ha sobrepasado el nodo objetivo."""
        if self.blanco:
            vec1 = self.blanco.posicion - self.nodo.posicion
            vec2 = self.posicion - self.nodo.posicion
            return vec2.magnitudCuadrada() >= vec1.magnitudCuadrada()
        return False

    def set_posicion(self):
        """Establece la posición al nodo actual."""
        self.posicion = self.nodo.posicion.copiar()

    def render(self, pantalla):
        """Dibuja el fantasma en la pantalla."""
        p = self.posicion.entero()
        pygame.draw.circle(pantalla, self.color, p, self.radio)
