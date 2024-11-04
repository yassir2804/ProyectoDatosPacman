
import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *
from PathFinder import PathFinder


class Blinky:
    def __init__(self, nodo, grafo, pacman=None):
        # Llama al constructor del padre primero
        super().__init__(nodo, pacman)

        # Propiedades específicas de Blinky
        self.nombre = BLINKY
        self.color = ROJO
        self.velocidad = 50 * ANCHOCELDA / 16
        self.radio = ANCHOCELDA // 2  # Radio ajustado al tamaño de la celda

        # Propiedades adicionales específicas de Blinky
        self.grafo = grafo
        self.pathfinder = PathFinder(grafo)
        self.esquina_scatter = None
        self.encontrar_esquina_scatter()

        # Inicializa movimiento
        self.iniciar_movimiento()

        # Cargar las skins para las diferentes direcciones
        self.skins = {
            ARRIBA: pygame.transform.scale(pygame.image.load("multimedia/BlinkyARRIBA.png").convert_alpha(),
                                           (self.radio * 2, self.radio * 2)),
            ABAJO: pygame.transform.scale(pygame.image.load("multimedia/BlinkyABAJO.png.png").convert_alpha(),
                                          (self.radio * 2, self.radio * 2)),
            IZQUIERDA: pygame.transform.scale(pygame.image.load("multimedia/BlinkyIZQUIERDA.png").convert_alpha(),
                                              (self.radio * 2, self.radio * 2)),
            DERECHA: pygame.transform.scale(pygame.image.load("multimedia/BlinkyDERECHA.png").convert_alpha(),
                                            (self.radio * 2, self.radio * 2)),
        }

        # Inicializar imagen actual
        self.imagen_actual = self.skins[DERECHA]

    def encontrar_esquina_scatter(self):
        """Encuentra el nodo más cercano a la esquina inferior derecha del mapa."""
        max_x = float('-inf')
        max_y = float('-inf')

        for (x, y) in self.grafo.nodosLUT.keys():
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

        col = max_x // ANCHOCELDA
        fila = max_y // ALTURACELDA
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

    def set_scatter_mode(self):
        """Activa el modo scatter y realiza los ajustes necesarios."""
        self.modo = SCATTER
        self.tiempo_scatter = self.duracion_scatter

        if self.esquina_scatter:
            mejor_direccion = self.pathfinder.encontrar_ruta(self.nodo, self.esquina_scatter, self.direccion)
            if mejor_direccion is not None:
                self.direccion = mejor_direccion
                self.blanco = self.nodo.vecinos[self.direccion]

    def iniciar_movimiento(self):
        """Inicia el movimiento del fantasma desde una posición estática."""
        direcciones_disponibles = self.obtener_direcciones_validas()
        if direcciones_disponibles:
            self.direccion = direcciones_disponibles[0]
            self.blanco = self.nodo.vecinos[self.direccion]

    def actualizar(self, dt, pacman):
        """Actualiza la posición y estado del fantasma."""
        if self.modo == SCATTER:
            self.tiempo_scatter -= dt
            if self.tiempo_scatter <= 0:
                self.modo = CHASE
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
        """Maneja la llegada a un nodo objetivo y decide la siguiente dirección."""
        self.nodo = self.blanco
        self.posicion = self.nodo.posicion.copiar()

        if self.nodo.vecinos.get(PORTAL):
            self.nodo = self.nodo.vecinos[PORTAL]
            self.set_posicion()

        if self.modo == SCATTER:
            self.actualizar_direccion_scatter()
        else:
            self.actualizar_direccion(pacman)

    def actualizar_direccion_scatter(self):
        """Actualiza la dirección cuando está en modo scatter."""
        if self.esquina_scatter is None:
            return

        mejor_direccion = self.pathfinder.encontrar_ruta(self.nodo, self.esquina_scatter, self.direccion)

        if mejor_direccion is not None:
            self.direccion = mejor_direccion
            self.blanco = self.nodo.vecinos[mejor_direccion]
        else:
            direcciones_validas = self.obtener_direcciones_validas()
            if direcciones_validas:
                self.direccion = direcciones_validas[0]
                self.blanco = self.nodo.vecinos[self.direccion]

    def actualizar_direccion(self, pacman):
        """Actualiza la dirección usando el PathFinder en modo persecución."""
        if pacman.nodo is None:
            return

        objetivo = pacman.nodo
        mejor_direccion = self.pathfinder.encontrar_ruta(self.nodo, objetivo, self.direccion)

        if mejor_direccion is not None:
            self.direccion = mejor_direccion
            self.blanco = self.nodo.vecinos[mejor_direccion]
        else:
            self.manejar_fallback(pacman)

    def manejar_fallback(self, pacman):
        """Maneja el caso cuando no se encuentra una ruta óptima."""
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
        # Elegir la imagen basada en la dirección actual
        if self.direccion in self.skins:
            self.skin = self.skins[self.direccion]
            pantalla.blit(self.skin, (p.x - self.radio_imagen, p.y - self.radio_imagen))
        else:
            pygame.draw.circle(pantalla, color_actual, p, self.radio)