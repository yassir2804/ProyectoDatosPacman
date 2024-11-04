import pygame
from numpy.random import random
from Constantes import *
from Entidad import *
from Modo import Controladora_Modos
from Grafo import *
class Fantasma(Entidad):
    def __init__(self, nodo,pacman=None):
        super().__init__(nodo)
        self.nombre = FANTASMA
        self.puntos = 200
        self.meta = Vector1(0,0)
        self.pacman=pacman
        self.modo= Controladora_Modos(self)

    def actualizar(self, dt):
        self.modo.actualizar(dt)
        if self.modo.current is SCATTER:
            self.scatter()
        elif self.modo.current is CHASE:
            self.chase()
        super().actualizar(dt)

    def chase(self):
        self.meta = self.pacman.posicion

    def scatter(self):
        self.meta =Vector1(0,0)

    def modo_normal(self):
        self.set_velocidad(100)
        self.metodoDireccion =self.direccion_meta

    def modo_Freight(self):
        self.modo.modo_freight()
        if self.modo.current == FREIGHT:
            self.set_velocidad(60)
            self.metodoDireccion = self.direccion_aleatoria
    
    def modo_Chase(self):
        self.modo.modo_chase()
        if self.modo.current == CHASE:
            self.scatter()


class Blinky(Fantasma):
    def __init__(self, nodo,pacman=None):
        # Call parent constructor first

    def iniciar_movimiento(self):
        """Inicia el movimiento del fantasma desde una posición estática."""
        direcciones_disponibles = self.obtener_direcciones_validas()
        if direcciones_disponibles:
            self.direccion = direcciones_disponibles[0]
            self.blanco = self.nodo.vecinos[self.direccion]

    def chase(self):
        """Override chase behavior to directly target Pacman."""
        if self.pacman and self.pacman.nodo:
            self.meta = self.pacman.nodo.posicion
            # Restaurar velocidad normal
            self.velocidad = 50 * ANCHOCELDA / 16

    def scatter(self):
        """Override scatter behavior to target corner."""
        if self.esquina_scatter:
            self.meta = self.esquina_scatter.posicion
            # Reducir la velocidad en modo scatter
            self.velocidad = self.velocidad

    def render(self, pantalla):
        """Método abstracto para renderizar el fantasma. Debe ser implementado por las subclases."""
        pass

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

    def set_posicion(self):
        """Establece la posición al nodo actual."""
        self.posicion = self.nodo.posicion.copiar()


class Blinky(Fantasma):
    def __init__(self, nodo, grafo, pacman=None):
        # Llama al constructor del padre primero
        super().__init__(nodo, pacman)

        # Propiedades específicas de Blinky
        self.nombre = BLINKY
        self.color = ROJO
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(0,0)

    def chase(self):
        self.meta = self.pacman.posicio

class Inky(Fantasma):
    def __init__(self, nodo,pacman=None):
        # Call parent constructor first
        super().__init__(nodo, pacman)

        # Override ghost properties
        self.nombre =INKY
        self.color = CELESTE
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(ANCHOCELDA*COLUMNAS,FILAS*ALTURACELDA)

    def chase(self):
        self.meta = self.pacman.posicion

class Clyde(Fantasma):
    def __init__(self, nodo,pacman=None):
        # Call parent constructor first
        super().__init__(nodo, pacman)

        # Override ghost properties
        self.nombre =CLYDE
        self.color = NARANJA
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(0,ANCHOCELDA*COLUMNAS)

    def chase(self):
        self.meta = self.pacman.posicion

class Pinky(Fantasma):
    def __init__(self, nodo,pacman=None):
        # Call parent constructor first
        super().__init__(nodo, pacman)

        # Override ghost properties
        self.nombre =PINKY
        self.color = ROSADO
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(ANCHOCELDA*COLUMNAS,0)

    def chase(self):
        self.meta = self.pacman.posicion
#
class GrupoFantasmas(object):
    def __init__(self,nodo,pacman):
        self.blinky = Blinky(nodo, pacman)
        self.pinky = Pinky(nodo, pacman)
        self.inky = Inky(nodo, pacman)
        self.clyde = Clyde(nodo, pacman)
        self.fantasmas = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.fantasmas)

    def actualizar(self, dt):
        for fantasmas in self:
            fantasmas.actualizar(dt)

    def scatter(self):
        for fantasmas in self:
            fantasmas.scatter()
    def modo_Freight(self):
        for fantasmas in self:
            fantasmas.modo_Freight()
        self.resetearPuntos()
        
    def modo_Chase(self):
        for fantasmas in self:
            fantasmas.modo_Chase()
            fantasmas.modo_normal()

    def setSpawnNode(self, node):
        for fantasmas in self:
            fantasmas.setSpawnNode(node)

    def actualizarPuntos(self):
        for fantasmas in self:
            fantasmas.puntos *= 2

    def resetearPuntos(self):
        for fantasmas in self:
            fantasmas.puntos = 200

    def reset(self):
        for fantasmas in self:
            fantasmas.reset()

    def esconder(self):
        for fantasmas in self:
            fantasmas.visible = False

    def show(self):
        for fantasmas in self:
            fantasmas.visible = True

    def render(self, screen):
        for fantasmas in self:
            fantasmas.render(screen)


        self.velocidad = 50 * ANCHOCELDA / 16
        self.radio = 24 // 2
        self.radio_colision = 5

        # Propiedades adicionales específicas de Blinky
        self.grafo = grafo
        self.pathfinder = PathFinder(grafo)
        self.esquina_scatter = None
        self.encontrar_esquina_scatter()

        # Inicializa movimiento
        self.iniciar_movimiento()

        # Cargar las skins para las diferentes direcciones
        self.skins = {
            ARRIBA: pygame.image.load("multimedia/BlinkyARRIBA.png").convert_alpha(),
            ABAJO: pygame.image.load("multimedia/BlinkyABAJO.png").convert_alpha(),
            IZQUIERDA: pygame.image.load("multimedia/BlinkyIZQUIERDA.png").convert_alpha(),
            DERECHA: pygame.image.load("multimedia/BlinkyDERECHA.png").convert_alpha()
        }

        # Escalar las imágenes al tamaño adecuado
        self.radio = ANCHOCELDA // 2
        for direccion in self.skins:
            # Escalar cada imagen al tamaño del radio de Blinky
            self.skins[direccion] = pygame.transform.scale(self.skins[direccion], (self.radio * 2, self.radio * 2))

        # Inicializar imagen actual
        self.imagen_actual = self.skins[DERECHA]

    def actualizar(self, dt):
        """Actualiza la posición del fantasma manteniendo alineación con la cuadrícula"""
        super().actualizar(dt)

        # Actualizar imagen según dirección
        if self.direccion in self.skins:
            self.imagen_actual = self.skins[self.direccion]

        if self.direccion == STOP:
            self.iniciar_movimiento()
            return

        if self.pacman and self.pacman.nodo is None:
            return

        # Calcular nueva posición
        vector_movimiento = self.direcciones[self.direccion] * self.velocidad * dt
        nueva_posicion = self.posicion + vector_movimiento

        # Forzar alineación con la cuadrícula
        if self.direccion in [IZQUIERDA, DERECHA]:
            # En movimiento horizontal, mantener la posición Y exacta del nodo
            nueva_posicion.y = self.nodo.posicion.y

            # Limitar el movimiento horizontal entre nodos
            if self.direccion == IZQUIERDA:
                nueva_posicion.x = max(nueva_posicion.x, self.blanco.posicion.x)
            else:  # DERECHA
                nueva_posicion.x = min(nueva_posicion.x, self.blanco.posicion.x)

        elif self.direccion in [ARRIBA, ABAJO]:
            # En movimiento vertical, mantener la posición X exacta del nodo
            nueva_posicion.x = self.nodo.posicion.x

            # Limitar el movimiento vertical entre nodos
            if self.direccion == ARRIBA:
                nueva_posicion.y = max(nueva_posicion.y, self.blanco.posicion.y)
            else:  # ABAJO
                nueva_posicion.y = min(nueva_posicion.y, self.blanco.posicion.y)

        self.posicion = nueva_posicion

        # Verificar si llegamos al siguiente nodo
        if self.blanco_sobrepasado():
            self.llegar_a_nodo()

    def llegar_a_nodo(self):
        """Handle node arrival and determine next direction using pathfinding."""
        self.nodo = self.blanco
        self.posicion = self.nodo.posicion.copiar()

        self.posicion.x = self.nodo.posicion.x
        self.posicion.y = self.nodo.posicion.y

        if self.nodo.vecinos.get(PORTAL):
            self.nodo = self.nodo.vecinos[PORTAL]
            self.set_posicion()

        # Use pathfinding to determine next direction
        if self.modo.current == SCATTER:
            self.actualizar_direccion_scatter()
        else:
            self.actualizar_direccion()

    def actualizar_direccion(self):
        """Update direction using pathfinding in chase mode."""
        if not self.pacman or not self.pacman.nodo:
            return

        mejor_direccion = self.pathfinder.encontrar_ruta(
            self.nodo,
            self.pacman.nodo,
            self.direccion
        )

        if mejor_direccion is not None:
            self.direccion = mejor_direccion
            self.blanco = self.nodo.vecinos[mejor_direccion]
        else:
            self.manejar_fallback()

    def actualizar_direccion_scatter(self):
        """Update direction in scatter mode."""
        if not self.esquina_scatter:
            return

        mejor_direccion = self.pathfinder.encontrar_ruta(
            self.nodo,
            self.esquina_scatter,
            self.direccion
        )

        if mejor_direccion is not None:
            self.direccion = mejor_direccion
            self.blanco = self.nodo.vecinos[mejor_direccion]
        else:
            direcciones_validas = self.obtener_direcciones_validas()
            if direcciones_validas:
                self.direccion = direcciones_validas[0]
                self.blanco = self.nodo.vecinos[self.direccion]

    def manejar_fallback(self):
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

            distancia = self.distancia_a_punto(nodo_siguiente.posicion, self.pacman.posicion)
            if distancia < menor_distancia:
                menor_distancia = distancia
                mejor_direccion = direccion

        if mejor_direccion is not None:
            self.direccion = mejor_direccion
            self.blanco = self.nodo.vecinos[mejor_direccion]
        elif direcciones_validas:
            self.direccion = direcciones_validas[0]
            self.blanco = self.nodo.vecinos[self.direccion]

    def encontrar_esquina_scatter(self):
        """Encuentra el nodo más cercano a la esquina inferior derecha del mapa."""
        max_x = float('-inf')
        max_y = float('-inf')

        # Encuentra las coordenadas máximas en X e Y
        for (x, y) in self.grafo.nodosLUT.keys():
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

        # Calcula la columna y la fila correspondientes
        col = max_x // ANCHOCELDA
        fila = max_y // ALTURACELDA

        # Intenta obtener el nodo en la esquina inferior derecha
        nodo_esquina = self.grafo.obtener_nodo_desde_tiles(col, fila)

        # Si no existe un nodo exacto, busca el nodo más cercano
        if nodo_esquina is None:
            menor_distancia = float('inf')
            for nodo in self.grafo.nodosLUT.values():
                distancia = abs(nodo.posicion.x - (col * ANCHOCELDA)) + \
                            abs(nodo.posicion.y - (fila * ALTURACELDA))
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    nodo_esquina = nodo

        self.esquina_scatter = nodo_esquina

    def render(self, pantalla):
        """Renderiza el fantasma centrado en su posición"""
        # Calcular la posición de renderizado centrada
        pos_render = self.posicion.entero()
        pos_render = (pos_render[0] - self.radio, pos_render[1] - self.radio)
        pantalla.blit(self.imagen_actual, pos_render)
