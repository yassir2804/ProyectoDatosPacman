import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *
from random import randint
from random import choice
from PathFinder import PathFinder


class Clyde(object):
    def __init__(self, nodo, grafo):
        self.nombre = CLYDE
        self.direcciones = {STOP: Vector1(0, 0), ARRIBA: Vector1(0, -1), ABAJO: Vector1(0, 1),
                            IZQUIERDA: Vector1(-1, 0), DERECHA: Vector1(1, 0)}
        self.direcciones_opuestas = {ARRIBA: ABAJO, ABAJO: ARRIBA, IZQUIERDA: DERECHA, DERECHA: IZQUIERDA, STOP: STOP}

        self.direccion = STOP
        self.velocidad = 85 * ANCHOCELDA / 16
        self.radio = 10
        self.color = NARANJA
        self.nodo = nodo
        self.setPosicion()
        self.blanco = nodo
        self.radioColision = 5
        self.grafo = grafo
        self.pathfinder = PathFinder(grafo)

        # Propiedades del modo scatter
        self.modo = CHASE
        self.tiempo_scatter = 0
        self.duracion_scatter = 7
        self.esquina_scatter = None
        self.encontrar_esquina_scatter()

        # Distancia umbral para cambiar comportamiento (8 bloques)
        self.distancia_umbral = 8 * ANCHOCELDA

    def encontrar_esquina_scatter(self):
        """Encuentra el nodo más cercano a la esquina inferior izquierda del mapa."""
        min_x = float('inf')
        max_y = float('-inf')

        # Encuentra el valor mínimo en X y máximo en Y para la esquina inferior izquierda
        for (x, y) in self.grafo.nodosLUT.keys():
            if x < min_x:
                min_x = x
            if y > max_y:
                max_y = y

        # Calcula la columna y la fila correspondientes a esta esquina
        col = min_x // ANCHOCELDA
        fila = max_y // ALTURACELDA

        # Obtén el nodo de la esquina inferior izquierda
        nodo_esquina = self.grafo.obtener_nodo_desde_tiles(col, fila)

        if nodo_esquina is None:
            menor_distancia = float('inf')
            for nodo in self.grafo.nodosLUT.values():
                distancia = abs(nodo.posicion.x - (col * ANCHOCELDA)) + \
                            abs(nodo.posicion.y - (fila * ALTURACELDA))
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    nodo_esquina = nodo

        self.esquina_scatter = nodo_esquina

    def calcular_distancia_a_pacman(self, pacman):
        """Calcula la distancia euclidiana entre Clyde y Pacman."""
        dx = self.posicion.x - pacman.posicion.x
        dy = self.posicion.y - pacman.posicion.y
        return (dx * dx + dy * dy) ** 0.5

    def actualizar(self, dt, pacman):
        if self.modo == SCATTER:
            self.tiempo_scatter -= dt
            if self.tiempo_scatter <= 0:
                self.modo = CHASE
                if self.direccion != STOP:
                    self.direccionReversa()

        # Comportamiento característico de Clyde
        if self.modo == CHASE:
            distancia = self.calcular_distancia_a_pacman(pacman)
            if distancia >= self.distancia_umbral:
                # Si está lejos, persigue a Pacman
                self.perseguir_objetivo(pacman.nodo)
            else:
                # Si está cerca, va a su esquina
                self.perseguir_objetivo(self.esquina_scatter)

        # Actualizar la posición
        self.posicion += self.direcciones[self.direccion] * self.velocidad * dt

        # Verificar si llegamos al nodo objetivo
        if self.overshotTarget():
            self.nodo = self.blanco

            # Manejar portales
            if self.nodo.vecinos.get(PORTAL) is not None:
                self.nodo = self.nodo.vecinos[PORTAL]

            # Actualizar dirección según el modo y la distancia
            if self.modo == CHASE:
                distancia = self.calcular_distancia_a_pacman(pacman)
                if distancia >= self.distancia_umbral:
                    self.perseguir_objetivo(pacman.nodo)
                else:
                    self.perseguir_objetivo(self.esquina_scatter)
            else:
                self.perseguir_objetivo(self.esquina_scatter)

            self.blanco = self.getNuevoBlanco(self.direccion)
            self.setPosicion()

    def perseguir_objetivo(self, nodo_objetivo):
        """Encuentra y establece la mejor dirección para alcanzar el objetivo."""
        mejor_direccion = self.pathfinder.encontrar_ruta(
            self.nodo,
            nodo_objetivo,
            self.direccion
        )

        if mejor_direccion is not None and self.validarDireccion(mejor_direccion):
            if not self.direccionOpuesta(mejor_direccion) or len(self.obtener_direcciones_validas()) == 1:
                self.direccion = mejor_direccion
        else:
            self.elegirDireccionAleatoria()

    def setPosicion(self):
        self.posicion = self.nodo.posicion.copiar()

    def validarDireccion(self, direccion):
        if direccion is not STOP:
            if self.nodo.vecinos[direccion] is not None:
                return True
        return False

    def getNuevoBlanco(self, direccion):
        if self.validarDireccion(direccion):
            return self.nodo.vecinos[direccion]
        return self.nodo

    def overshotTarget(self):
        if self.blanco is not None:
            vec1 = self.blanco.posicion - self.nodo.posicion
            vec2 = self.posicion - self.nodo.posicion
            nodo2Blanco = vec1.magnitudCuadrada()
            nodo2Self = vec2.magnitudCuadrada()
            return nodo2Self >= nodo2Blanco
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

    def obtener_direcciones_validas(self):
        """Obtiene todas las direcciones válidas desde el nodo actual."""
        direcciones_validas = []
        for direccion in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]:
            if self.validarDireccion(direccion):
                direcciones_validas.append(direccion)
        return direcciones_validas

    def elegirDireccionAleatoria(self):
        """Elige una dirección aleatoria válida, evitando la dirección opuesta si es posible."""
        direcciones_posibles = []
        for direccion in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]:
            if self.validarDireccion(direccion) and not self.direccionOpuesta(direccion):
                direcciones_posibles.append(direccion)

        if not direcciones_posibles:
            direcciones_posibles = self.obtener_direcciones_validas()

        if direcciones_posibles:
            self.direccion = choice(direcciones_posibles)
        else:
            self.direccion = STOP

    def render(self, pantalla):
        p = self.posicion.entero()
        color_actual = PURPURA if self.modo == SCATTER else self.color
        pygame.draw.circle(pantalla, color_actual, p, self.radio)