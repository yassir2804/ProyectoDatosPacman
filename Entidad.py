import pygame
from Vector import Vector1
from Constantes import *
from random import randint
import heapq


# Clase principal que representa una entidad en el juego
class Entidad(object):
    def __init__(self, nodo):
        # Inicialización de atributos básicos
        self.nombre = None
        # Diccionario de vectores de dirección (arriba, abajo, izquierda, derecha, parar)
        self.direcciones = {STOP: Vector1(0, 0), ARRIBA: Vector1(0, -1), ABAJO: Vector1(0, 1),
                            IZQUIERDA: Vector1(-1, 0), DERECHA: Vector1(1, 0)}
        # Diccionario de direcciones opuestas
        self.direcciones_opuestas = {ARRIBA: ABAJO, ABAJO: ARRIBA, IZQUIERDA: DERECHA, DERECHA: IZQUIERDA, STOP: STOP}
        self.direccion = STOP
        self.set_velocidad(150)  # Velocidad inicial
        self.radio = 10  # Radio visual de la entidad
        self.radio_colision = 5  # Radio para detección de colisiones
        self.visible = True
        self.desactivar_portal = False
        self.metodo_direccion = self.direccion_meta
        self.set_nodo_inicio(nodo)
        self.meta = Vector1(0, 0)

        # Atributos para animación
        self.animation_timer = 0
        self.animation_interval = 0.05
        self.skins = {}
        self.skin_index = 0
        self.skin = None
        self.usar_skin_especial = False
        self.skin_especial = None

        # Sistema de caché para pathfinding
        self.cached_paths = {}
        self.path_timestamp = 0
        self.max_cache_age = 30

    # Calcula la distancia Manhattan entre dos posiciones
    def calcular_distancia_manhattan(self, pos1, pos2):
        diferencia = pos2 - pos1
        return abs(diferencia.x) + abs(diferencia.y)

        # ============= SISTEMA DE PATHFINDING GENERADO POR IA =============
        # Este metodo implementa el algoritmo A* (A-star) generado por IA para encontrar el camino óptimo
        # entre dos nodos. A* es un algoritmo de búsqueda informada que combina:
        # - El costo real del camino desde el inicio (g_score)
        # - Una estimación heurística hasta la meta (h_score usando distancia Manhattan)

    def encontrar_camino_optimo(self, inicio, meta):
        """
        Implementación del algoritmo A* optimizada por IA para encontrar el mejor camino.
        Utiliza una cola de prioridad (heap) para seleccionar siempre el nodo más prometedor
        y un contador para desempatar nodos con el mismo f_score, garantizando estabilidad.

        Características especiales de esta implementación IA:
        - Uso de Vector1 para cálculos de posición y distancia
        - Sistema de prioridad con desempate para nodos iguales
        - Optimización de memoria usando diccionarios para trackear nodos
        - Reconstrucción eficiente del camino almacenando solo la primera dirección
        """
        if not inicio or not meta:
            return None

        from itertools import count
        contador = count()

        # Cola de prioridad: (f_score, contador, nodo)
        # f_score = g_score (costo real) + h_score (heurística)
        # contador garantiza que nodos con igual f_score se procesen en orden FIFO
        frontera = [(0, next(contador), inicio)]
        heapq.heapify(frontera)

        # Diccionarios para trackear el camino y los costos
        vino_de = {inicio: None}  # Mapea nodo -> (nodo_anterior, direccion)
        g_score = {inicio: 0}  # Costo real desde el inicio
        f_scores = {inicio: self.calcular_distancia_manhattan(inicio.posicion, meta.posicion)}

        while frontera:
            _, _, actual = heapq.heappop(frontera)

            # Si llegamos a la meta, terminamos
            if actual == meta:
                break

            # Explorar las cuatro direcciones posibles
            for direccion in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]:
                if actual.vecinos[direccion] is not None and self.validar_direccion(direccion):
                    vecino = actual.vecinos[direccion]

                    # Calcular el costo real hasta el vecino
                    costo_movimiento = (vecino.posicion - actual.posicion).magnitud()
                    tentative_g_score = g_score[actual] + costo_movimiento

                    # Si encontramos un mejor camino al vecino
                    if vecino not in g_score or tentative_g_score < g_score[vecino]:
                        vino_de[vecino] = (actual, direccion)
                        g_score[vecino] = tentative_g_score

                        # Calcular f_score = g_score + h_score (heurística)
                        h_score = self.calcular_distancia_manhattan(vecino.posicion, meta.posicion)
                        f_score = tentative_g_score + h_score
                        f_scores[vecino] = f_score

                        # Añadir a la frontera con prioridad basada en f_score
                        heapq.heappush(frontera, (f_score, next(contador), vecino))

        # Si no hay camino a la meta
        if meta not in vino_de:
            return None

        # Reconstruir el camino para obtener la primera dirección
        actual = meta
        while vino_de[actual][0] != inicio:
            actual = vino_de[actual][0]
        return vino_de[actual][1]

        # Este metodo determina la mejor dirección hacia la meta usando el pathfinding A*
        # y considera la existencia de portales como atajos en el mapa

    def direccion_meta(self, direcciones):
        """
        Sistema de navegación inteligente generado por IA que:
        1. Utiliza caché para optimizar búsquedas repetidas
        2. Considera portales como atajos (70% de la distancia normal)
        3. Combina pathfinding A* con heurísticas de distancia
        4. Implementa un sistema de fallback cuando A* no encuentra ruta
        """
        if not direcciones:
            return STOP

        # Comprobar si hay un camino en caché válido
        cache_key = (id(self.nodo), self.meta.x, self.meta.y)  # Usar id() para el nodo
        tiempo_actual = pygame.time.get_ticks() / 1000

        if cache_key in self.cached_paths:
            direccion_cached, timestamp = self.cached_paths[cache_key]
            if tiempo_actual - timestamp < self.max_cache_age:
                if direccion_cached in direcciones:
                    return direccion_cached

        # Encontrar el nodo meta más cercano a la posición meta
        mejor_nodo_meta = None
        menor_distancia = float('inf')

        # Buscar en los nodos vecinos cuál está más cerca de la meta
        for direccion in direcciones:
            nodo_vecino = self.nodo.vecinos[direccion]
            if nodo_vecino:
                # Considerar portales
                if nodo_vecino.vecinos[PORTAL] is not None:
                    nodo_portal = nodo_vecino.vecinos[PORTAL]
                    distancia = (nodo_portal.posicion - self.meta).magnitudCuadrada()
                    # Aplicar bonus a rutas con portales
                    distancia *= 0.7
                else:
                    distancia = (nodo_vecino.posicion - self.meta).magnitudCuadrada()

                if distancia < menor_distancia:
                    menor_distancia = distancia
                    mejor_nodo_meta = nodo_vecino

        if mejor_nodo_meta is None:
            return STOP

        # Usar A* para encontrar la mejor dirección
        mejor_direccion = self.encontrar_camino_optimo(self.nodo, mejor_nodo_meta)

        if mejor_direccion is None or mejor_direccion not in direcciones:
            # Si A* no encuentra camino válido, usar el metodo de distancia directa
            mejor_direccion = direcciones[0]
            mejor_distancia = float('inf')

            for direccion in direcciones:
                vector_direccion = self.direcciones[direccion]
                siguiente_pos = self.nodo.posicion + (vector_direccion * ANCHOCELDA)
                siguiente_nodo = self.nodo.vecinos[direccion]

                if siguiente_nodo and siguiente_nodo.vecinos[PORTAL] is not None:
                    pos_despues_portal = siguiente_nodo.vecinos[PORTAL].posicion
                    nueva_distancia = (pos_despues_portal - self.meta).magnitudCuadrada()
                    nueva_distancia *= 0.7  # Bonus para portales
                else:
                    nueva_distancia = (siguiente_pos - self.meta).magnitudCuadrada()

                if nueva_distancia < mejor_distancia:
                    mejor_distancia = nueva_distancia
                    mejor_direccion = direccion

        # Guardar en caché el resultado usando una clave que sea hasheable
        self.cached_paths[cache_key] = (mejor_direccion, tiempo_actual)
        self.path_timestamp = tiempo_actual

        return mejor_direccion

    #Metodo que hereda a las entidades la actualizacion de skin
    def actualizar_skin(self):

        if self.usar_skin_especial and self.skin_especial is not None:
            self.skin = self.skin_especial
            return

        if self.direccion in self.skins and len(self.skins[self.direccion]) > 0:
            self.skin_index = (self.skin_index + 1) % len(self.skins[self.direccion])
            self.skin = self.skins[self.direccion][self.skin_index]


    #Metodo que hereda la actualizacion de animacion basado en el tiempo
    def actualizar_animacion(self, dt):

        if not self.skins and not self.usar_skin_especial:
            return

        self.animation_timer += dt
        if self.animation_timer >= self.animation_interval:
            self.animation_timer = 0
            self.actualizar_skin()

    #Es un metodo que reinicia a las entidades
    def reset(self):
        self.set_nodo_inicio(self.nodo_inicio)
        self.direccion = STOP
        self.visible = True

    #Metodo para poner a las entidades entre nodos
    def establecer_entre_nodos(self, direccion):

        if self.nodo.vecinos[direccion] is not None:
            self.blanco = self.nodo.vecinos[direccion]
            self.posicion = (self.nodo.posicion + self.blanco.posicion) / 2.0

    #Establece la posicion actual de la entidad
    def set_posicion(self):
        self.posicion = self.nodo.posicion.copiar()


    #Actualiza la posición y estado de la entidad.
    def actualizar(self, dt):

        self.posicion += self.direcciones[self.direccion] * self.velocidad * dt

        if self.blanco_sobrepasado():
            self.nodo = self.blanco

            direcciones = self.obtener_direcciones_validas()
            direccion = self.metodo_direccion(direcciones)

            if not self.desactivar_portal:
                if self.nodo.vecinos[PORTAL] is not None:
                    self.nodo = self.nodo.vecinos[PORTAL]

            self.blanco = self.get_nuevo_blanco(direccion)

            if self.blanco is not self.nodo:
                self.direccion = direccion
            else:
                self.blanco = self.get_nuevo_blanco(self.direccion)

            self.set_posicion()

    #Obtiene todas las direcciones válidas desde el nodo actual

    def obtener_direcciones_validas(self):

        direcciones = []
        for direccion in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]:
            if self.validar_direccion(direccion):
                if not self.direccion_opuesta(direccion):
                    direcciones.append(direccion)

        if len(direcciones) == 0:
            direccion_opuesta = self.direcciones_opuestas[self.direccion]
            if self.validar_direccion(direccion_opuesta):
                direcciones.append(direccion_opuesta)

        return direcciones

   #Verifica si una dirección es válida desde el nodo actual
    def validar_direccion(self, direccion):

        if direccion is not STOP:
            if self.nombre in self.nodo.acceso[direccion]:
                if self.nodo.vecinos[direccion] is not None:
                    return True
        return False

    #Obtiene el siguiente nodo blanco basado en la dirección

    def get_nuevo_blanco(self, direccion):

        if self.validar_direccion(direccion):
            return self.nodo.vecinos[direccion]
        return self.nodo

    #Obtiene el siguiente nodo blanco basado en la dirección

    def blanco_sobrepasado(self):
        if self.blanco is not None:
            vec1 = self.blanco.posicion - self.nodo.posicion
            vec2 = self.posicion - self.nodo.posicion
            nodo2_blanco = vec1.magnitudCuadrada()
            nodo2_self = vec2.magnitudCuadrada()

            return nodo2_self >= nodo2_blanco
        return False

    #Invierte la dirección actual de la entidad

    def direccion_reversa(self):

        self.direccion *= -1
        temp = self.nodo
        self.nodo = self.blanco
        self.blanco = temp

    #Verifica si una dirección es opuesta a la dirección actual

    def direccion_opuesta(self, direccion):

        if direccion is not STOP:
            if direccion == self.direccion * -1:
                return True
        return False

    #Establece la velocidad de la entidad
    def set_velocidad(self, velocidad):
        self.velocidad = velocidad

    #Selecciona una dirección aleatoria de la lista de direcciones proporcionada
    def direccion_aleatoria(self, direcciones):

        if not direcciones:
            return STOP

        return direcciones[randint(0, len(direcciones) - 1)]

    def set_nodo_inicio(self, nodo):
        self.nodo=nodo
        self.blanco=nodo
        self.nodo_inicio =nodo
        self.set_posicion()
