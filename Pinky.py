import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *

class Pinky:
    def __init__(self, nodo, grafo):
        self.nombre = PINKY
        self.direcciones = {STOP: Vector1(0, 0),ARRIBA: Vector1(0, -1),ABAJO: Vector1(0, 1),IZQUIERDA: Vector1(-1, 0),DERECHA: Vector1(1, 0)}
        self.direcciones_opuestas = {ARRIBA: ABAJO,ABAJO: ARRIBA,IZQUIERDA: DERECHA,DERECHA: IZQUIERDA, STOP: STOP}

        self.direccion = STOP
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.color = ROSADO
        self.nodo = nodo
        self.set_posicion()
        self.blanco = nodo
        self.radio_colision = 5
        self.grafo = grafo
        self.pathfinder = PathFinder(grafo)

        # Propiedades del modo scatter
        self.modo = CHASE
        self.tiempo_scatter = 0
        self.duracion_scatter = 7
        self.esquina_scatter = None
        self.encontrar_esquina_scatter()

        #Inicio para poder moverse
        self.iniciar_movimiento()
    def encontrar_esquina_scatter(self):
        """Encuentra el nodo más cercano a la esquina inferior izquierda del mapa."""
        min_x = float('inf')  # Cambiado para buscar el mínimo en X
        mix_y = -float('inf')  # Buscando el máximo en Y

        # Encuentra las coordenadas mínimas en X y máximas en Y.
        for (x, y) in self.grafo.nodosLUT.keys():
            if x < min_x:
                min_x = x
            if y < mix_y:
                mix_y = y

            col = min_x // ANCHOCELDA  # Columna de la esquina superior izquierda
            fila = mix_y // ALTURACELDA  # Fila de la esquina superior izquierda

            nodo_esquina = self.grafo.obtener_nodo_desde_tiles(col, fila)

            if nodo_esquina is None:
                menor_distancia = float('inf')
                for nodo in self.grafo.nodosLUT.values():
                    distancia = abs(nodo.posicion.x - (col * ANCHOCELDA)) + abs(nodo.posicion.y - (fila * ALTURACELDA))
                    if distancia < menor_distancia:
                        menor_distancia = distancia
                        nodo_esquina = nodo

            self.esquina_scatter = nodo_esquina

    def set_scatter_mode(self):
        """Activa el modo scatter y realiza los ajustes necesarios."""
        self.modo = SCATTER
        self.tiempo_scatter = self.duracion_scatter

        # Forzar la dirección inicial hacia la esquina scatter
        if self.esquina_scatter:
            mejor_direccion = self.pathfinder.encontrar_ruta(self.nodo, self.esquina_scatter, self.direccion)
            if mejor_direccion is not None:
                self.direccion = mejor_direccion
                self.blanco = self.nodo.vecinos[self.direccion]
    def calcular_objetivo(self, pacman):
        """Calcula el punto objetivo 4 casillas por delante de Pacman"""
        if pacman.direccion == STOP or pacman.nodo is None:
            return pacman.nodo

        # Calculamos la posición objetivo en tiles (cuadros del laberinto)
        pos_actual = (pacman.posicion.x // ANCHOCELDA, pacman.posicion.y // ALTURACELDA)

        # Vector de dirección en tiles
        vector_direccion = self.direcciones[pacman.direccion]
        objetivo_x = pos_actual[0]
        objetivo_y = pos_actual[1]

        # Ajustamos la posición objetivo según la dirección
        if pacman.direccion == ARRIBA:
            # Implementamos el "bug" del Pac-Man original
            objetivo_x -= 4  # 4 casillas a la izquierda
            objetivo_y -= 4  # 4 casillas arriba
        elif pacman.direccion == ABAJO:
            objetivo_y += 4
        elif pacman.direccion == IZQUIERDA:
            objetivo_x -= 4
        elif pacman.direccion == DERECHA:
            objetivo_x += 4

        # Intentamos obtener el nodo más cercano a la posición objetivo
        nodo_objetivo = self.grafo.obtener_nodo_desde_tiles(int(objetivo_x), int(objetivo_y))

        # Si no encontramos un nodo válido, buscamos el nodo más cercano
        if nodo_objetivo is None:
            menor_distancia = float('inf')
            posicion_objetivo = Vector1(objetivo_x * ANCHOCELDA, objetivo_y * ALTURACELDA)

            for nodo in self.grafo.nodosLUT.values():
                distancia = self.distancia_a_punto(nodo.posicion, posicion_objetivo)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    nodo_objetivo = nodo

        return nodo_objetivo if nodo_objetivo else pacman.nodo

    def iniciar_movimiento(self):
        """Inicia el movimiento del fantasma."""
        direcciones_disponibles = self.obtener_direcciones_validas()
        if direcciones_disponibles:
            self.direccion = direcciones_disponibles[0]
            self.blanco = self.nodo.vecinos[self.direccion]

    def actualizar(self, dt, pacman):
        """Actualiza la posición del fantasma."""
        if self.modo == SCATTER:
            self.tiempo_scatter -= dt
            if self.tiempo_scatter <= 0:
                self.modo = CHASE
                # Invertir dirección al salir del modo scatter
                if self.direccion != STOP:
                    self.direccion = self.direcciones_opuestas[self.direccion]
        if self.direccion == STOP:
            self.iniciar_movimiento()
            return

        if pacman.nodo is None:
            return

        vector_movimiento = self.direcciones[self.direccion] * self.velocidad * dt
        nueva_posicion = self.posicion + vector_movimiento

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

        if self.nodo.vecinos.get(PORTAL):
            self.nodo = self.nodo.vecinos[PORTAL]
            self.set_posicion()

        self.actualizar_direccion(pacman)

    def actualizar_direccion(self, pacman):
        """Actualiza la dirección usando el PathFinder hacia el punto objetivo."""
        if pacman.nodo is None:
            return

        nodo_objetivo = self.calcular_objetivo(pacman)

        if nodo_objetivo is None:
            nodo_objetivo = pacman.nodo

        mejor_direccion = self.pathfinder.encontrar_ruta(
            self.nodo,
            nodo_objetivo,
            self.direccion
        )

        if mejor_direccion is not None:
            self.direccion = mejor_direccion
            self.blanco = self.nodo.vecinos[mejor_direccion]
        else:
            # Comportamiento de fallback
            direcciones_validas = self.obtener_direcciones_validas()
            mejor_direccion = None
            menor_distancia = float('inf')

            for direccion in direcciones_validas:
                if self.direccion != STOP and direccion == self.direcciones_opuestas[self.direccion]:
                    continue

                nodo_siguiente = self.nodo.vecinos[direccion]
                if nodo_siguiente is None:
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
        """Calcula la distancia euclidiana entre dos puntos."""
        return (pos1 - pos2).magnitud()

    def obtener_direcciones_validas(self):
        """Obtiene todas las direcciones válidas disponibles."""
        return [direccion for direccion in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]
                if self.nodo.vecinos.get(direccion) is not None and
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
        color_actual = PURPURA if self.modo == SCATTER else self.color
        pygame.draw.circle(pantalla, color_actual, p, self.radio)