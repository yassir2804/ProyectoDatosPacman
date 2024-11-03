
from Pacman import *
from numpy.random import random
from Constantes import *
from Entidad import *
from Modo import Controladora_Modos
from PathFinder import PathFinder
class Fantasma(Entidad):
    def __init__(self, nodo,pacman=None):
        Entidad.__init__(self, nodo)
        self.nombre = FANTASMA
        self.puntos = 200
        self.meta = Vector1(0,0)
        self.metodoDireccion = self.direccion_meta
        self.pacman=pacman
        self.modo= Controladora_Modos(self)

    def actualizar(self, dt):
        self.modo.actualizar(dt)
        if self.modo.current is SCATTER:
            self.scatter()
        elif self.modo.current is CHASE:
            self.chase()
        Entidad.actualizar(self, dt)

    def iniciar_movimiento(self):
        """Inicia el movimiento del fantasma desde una posición estática."""
        direcciones_disponibles = self.obtener_direcciones_validas()
        if direcciones_disponibles:
            self.direccion = direcciones_disponibles[0]
            self.blanco = self.nodo.vecinos[self.direccion]
    
    def chase(self):
        """Override chase behavior to directly target Pacman"""
        if self.pacman and self.pacman.nodo:
            self.meta = self.pacman.nodo.posicion
            # Restaurar velocidad normal
            self.velocidad = 50 * ANCHOCELDA / 16

    def scatter(self):
        """Override scatter behavior to target corner"""
        if self.esquina_scatter:
            self.meta = self.esquina_scatter.posicion
            # Reducir la velocidad en modo scatter
            self.velocidad = self.velocidad

    def render(self, pantalla):
        """Actualizado para mostrar diferentes colores según el modo"""
        p = self.posicion.entero()

        # Color según el modo
       # if self.modo.current == SCATTER:
            # Parpadeo en modo scatter
           # tiempo = pygame.time.get_ticks() / 200  # Ajusta la velocidad del parpadeo
            #if int(tiempo) % 2 == 0:
                #color_actual = PURPURA
        #else:
                #color_actual = BLANCO
        #else:
            #color_actual = self.color

        pygame.draw.circle(pantalla, self.color, p, self.radio)

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
        # Call parent constructor first
        super().__init__(nodo, pacman)

        # Override ghost properties
        self.nombre = BLINKY
        self.color = ROJO
        self.velocidad = 50 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

        # Additional Blinky-specific properties
        self.grafo = grafo
        self.pathfinder = PathFinder(grafo)
        self.esquina_scatter = None
        self.encontrar_esquina_scatter()

        # Initialize movement
        self.iniciar_movimiento()


    def actualizar(self, dt):
        """Override update to use pathfinding"""
        super().actualizar(dt)

        if self.direccion == STOP:
            self.iniciar_movimiento()
            return

        if self.pacman and self.pacman.nodo is None:
            return

        vector_movimiento = self.direcciones[self.direccion] * self.velocidad * dt
        nueva_posicion = self.posicion + vector_movimiento

        # Maintain alignment
        if self.direccion in [IZQUIERDA, DERECHA]:
            nueva_posicion.y = self.nodo.posicion.y
        else:
            nueva_posicion.x = self.nodo.posicion.x

        self.posicion = nueva_posicion

        if self.blanco_sobrepasado():
            self.llegar_a_nodo()

    def llegar_a_nodo(self):
        """Handle node arrival and determine next direction using pathfinding"""
        self.nodo = self.blanco
        self.posicion = self.nodo.posicion.copiar()

        if self.nodo.vecinos.get(PORTAL):
            self.nodo = self.nodo.vecinos[PORTAL]
            self.set_posicion()

        # Use pathfinding to determine next direction
        if self.modo.current == SCATTER:
            self.actualizar_direccion_scatter()
        else:
            self.actualizar_direccion()

    def actualizar_direccion(self):
        """Update direction using pathfinding in chase mode"""
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
        """Update direction in scatter mode"""
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