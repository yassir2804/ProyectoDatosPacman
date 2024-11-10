import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *
from random import randint

from collections import defaultdict
import heapq
import pygame
from Vector import Vector1



class Entidad(object):
    def __init__(self, nodo):
        self.nombre = None
        self.direcciones = {STOP: Vector1(0, 0), ARRIBA: Vector1(0, -1), ABAJO: Vector1(0, 1),IZQUIERDA: Vector1(-1, 0), DERECHA: Vector1(1, 0)}
        self.direcciones_opuestas = {ARRIBA: ABAJO, ABAJO: ARRIBA, IZQUIERDA: DERECHA, DERECHA: IZQUIERDA, STOP: STOP}
        self.direccion = STOP
        self.set_velocidad(150)
        self.radio = 10
        self.radio_colision = 5
        self.color = BLANCO
        self.visible = True
        self.desactivar_portal = False
        self.metodo_direccion = self.direccion_meta
        self.set_nodo_inicio(nodo)

        # Sistema de animación mejorado
        self.animation_timer = 0
        self.animation_interval = 0.05
        self.skins = {}
        self.skin_index = 0
        self.skin = None
        self.usar_skin_especial = False  # Nuevo flag para control de skins especiales
        self.skin_especial = None  # Para al
        self.cached_paths = {}
        self.path_timestamp = 0
        self.max_cache_age = 30

    def calcular_distancia_manhattan(self, pos1, pos2):
        """Calcula la distancia Manhattan usando Vector1"""
        diferencia = pos2 - pos1
        return abs(diferencia.x) + abs(diferencia.y)

    def calcular_hash_estado(self, nodo_origen, nodo_destino):
        """Genera un hash único aprovechando el __hash__ de Vector1"""
        return hash((nodo_origen.posicion.__hash__(),
                     nodo_destino.posicion.__hash__()))

    def encontrar_camino_optimo(self, inicio, meta):
        """A* optimizado para usar Vector1"""
        if not inicio or not meta:
            return None

        # Usar tupla (f_score, h_score, nodo) para desempate en el heap
        frontera = [(0, self.calcular_distancia_manhattan(inicio.posicion, meta.posicion), inicio)]
        heapq.heapify(frontera)

        vino_de = {inicio: None}
        g_score = {inicio: 0}  # Costo real desde el inicio

        while frontera:
            _, _, actual = heapq.heappop(frontera)

            if actual == meta:
                break

            for direccion in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]:
                if actual.vecinos[direccion] is not None and self.validar_direccion(direccion):
                    vecino = actual.vecinos[direccion]
                    # Usar Vector1 para calcular el costo del movimiento
                    costo_movimiento = (vecino.posicion - actual.posicion).magnitud()
                    tentative_g_score = g_score[actual] + costo_movimiento

                    if vecino not in g_score or tentative_g_score < g_score[vecino]:
                        vino_de[vecino] = (actual, direccion)
                        g_score[vecino] = tentative_g_score

                        h_score = self.calcular_distancia_manhattan(vecino.posicion, meta.posicion)
                        f_score = tentative_g_score + h_score
                        heapq.heappush(frontera, (f_score, h_score, vecino))

        # Reconstruir el camino
        if meta not in vino_de:
            return None

        # Recuperar la primera dirección del camino
        actual = meta
        while vino_de[actual][0] != inicio:
            actual = vino_de[actual][0]
        return vino_de[actual][1]

    def direccion_meta(self, direcciones):
        if not direcciones:
            return STOP

        mejor_distancia = float('inf')
        mejor_direccion = direcciones[0]

        for direccion in direcciones:
            # Simular el siguiente movimiento
            vector_direccion = self.direcciones[direccion]
            siguiente_pos = self.nodo.posicion + (vector_direccion * ANCHOCELDA)
            siguiente_nodo = self.nodo.vecinos[direccion]

            # Verificar si hay un portal disponible en el siguiente nodo
            if siguiente_nodo and siguiente_nodo.vecinos[PORTAL] is not None:
                # Si hay portal, usar la posición después del portal para el cálculo
                pos_despues_portal = siguiente_nodo.vecinos[PORTAL].posicion
                nueva_distancia = (pos_despues_portal - self.meta.posicion).magnitudCuadrada()
            else:
                # Si no hay portal, usar la distancia normal
                nueva_distancia = (siguiente_pos - self.meta.posicion).magnitudCuadrada()

            # Factor de bonus para favorecer rutas con portales
            if siguiente_nodo and siguiente_nodo.vecinos[PORTAL] is not None:
                nueva_distancia *= 0.7  # Reducir la distancia percibida para favorecer el uso del portal

            if nueva_distancia < mejor_distancia:
                mejor_distancia = nueva_distancia
                mejor_direccion = direccion

        return mejor_direccion

    def limpiar_cache(self):
        """Limpia el caché de caminos antiguos"""
        tiempo_actual = pygame.time.get_ticks() / 1000
        self.cached_paths = {k: v for k, v in self.cached_paths.items()
                             if tiempo_actual - self.path_timestamp < self.max_cache_age}

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

    def render(self, pantalla):
        """Dibuja la entidad en la pantalla."""
        if self.visible:
            p = self.posicion.entero()
            pygame.draw.circle(pantalla,self.color, p, self.radio)

    def direccion_aleatoria(self, direcciones):
        """Selecciona una dirección aleatoria de la lista de direcciones proporcionada."""
        if not direcciones:
            return STOP

        return direcciones[randint(0, len(direcciones) - 1)]

    def direccion_meta(self, direcciones):
        """Versión avanzada que considera múltiples factores para elegir la mejor dirección"""
        if not direcciones:
            return STOP

        # Pesos para diferentes factores (ajustar según necesidad)
        PESOS = {
            'distancia': 1.0,  # Peso para la distancia directa
            'progreso': 1.5,  # Peso para el progreso hacia el objetivo
            'inercia': 0.5,  # Peso para mantener la dirección actual
            'esquinas': 0.3  # Peso para evitar esquinas
        }

        mejor_puntuacion = float('inf')
        mejor_direccion = STOP

        # Calculamos la distancia actual al objetivo
        distancia_resta = self.nodo.posicion - self.meta
        distancia_actual = distancia_resta.magnitudCuadrada()

        for direccion in direcciones:
            # Calculamos la siguiente posición si tomamos esta dirección
            siguiente_pos = self.nodo.posicion + self.direcciones[direccion] * ANCHOCELDA
            siguiente_nodo = self.nodo.vecinos[direccion]

            # 1. Puntuación por distancia al objetivo
            nueva_distancia = (siguiente_pos - self.meta).magnitudCuadrada()
            puntuacion_distancia = nueva_distancia

            # 2. Puntuación por progreso (qué tanto nos acercamos al objetivo)
            # Si nueva_distancia es menor que distancia_actual, estamos progresando
            puntuacion_progreso = nueva_distancia - distancia_actual

            # 3. Puntuación por inercia (preferir mantener la dirección actual)
            puntuacion_inercia = 0 if direccion == self.direccion else 100

            # 4. Puntuación por esquinas (evitar callejones sin salida)
            puntuacion_esquinas = 0
            if siguiente_nodo:
                # Contamos cuántas salidas tiene el siguiente nodo
                salidas_validas = sum(1 for d in [ARRIBA, ABAJO, IZQUIERDA, DERECHA]
                                      if siguiente_nodo.vecinos[d] is not None)
                puntuacion_esquinas = 50 * (4 - salidas_validas)  # Penalizar nodos con pocas salidas

            # Calculamos la puntuación final (menor es mejor)
            puntuacion_final = (
                    PESOS['distancia'] * puntuacion_distancia +
                    PESOS['progreso'] * puntuacion_progreso +
                    PESOS['inercia'] * puntuacion_inercia +
                    PESOS['esquinas'] * puntuacion_esquinas
            )

            # Actualizamos la mejor dirección si encontramos una mejor puntuación
            if puntuacion_final < mejor_puntuacion:
                mejor_puntuacion = puntuacion_final
                mejor_direccion = direccion

        return mejor_direccion


    def set_nodo_inicio(self, nodo):
        self.nodo=nodo
        self.blanco=nodo
        self.nodo_inicio =nodo
        self.set_posicion()
