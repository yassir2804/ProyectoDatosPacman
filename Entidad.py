import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *
from random import randint

class Entidad(object):
    def __init__(self, nodo):
        self.nombre = None
        self.direcciones = {STOP: Vector1(0, 0), ARRIBA: Vector1(0, -1), ABAJO: Vector1(0, 1),IZQUIERDA: Vector1(-1, 0), DERECHA: Vector1(1, 0)}
        self.direcciones_opuestas = {ARRIBA: ABAJO, ABAJO: ARRIBA, IZQUIERDA: DERECHA, DERECHA: IZQUIERDA, STOP: STOP}
        self.direccion = STOP
        self.set_velocidad(100)
        self.radio = 10
        self.radio_colision = 5
        self.color = BLANCO
        self.nodo = nodo
        self.nodo_inicio(nodo)
        self.set_posicion()
        self.blanco = nodo
        self.visible = True
        self.desactivar_portal = False
        self.metodo_direccion = self.direccion_meta
        self.animation_timer = 0
        self.animation_interval = 0.05  # 50ms entre frames
        self.skins = {}  # Diccionario para almacenar las animaciones
        self.skin_index = 0
        self.skin = None

    def actualizar_animacion(self, dt):
        """Actualiza el frame de la animación basado en el tiempo transcurrido"""
        if not self.skins:  # Si no hay skins cargadas, no actualizar
            return

        self.animation_timer += dt
        if self.animation_timer >= self.animation_interval:
            self.animation_timer = 0
            self.actualizar_skin()

    def actualizar_skin(self):
        """Actualiza al siguiente frame de la animación actual"""
        if self.direccion in self.skins:
            self.skin_index = (self.skin_index + 1) % len(self.skins[self.direccion])
            self.skin = self.skins[self.direccion][self.skin_index]


    def establecer_entre_nodos(self, direccion):
        """Coloca la fruta exactamente en medio de dos nodos"""
        if self.nodo.vecinos[direccion] is not None:
            self.blanco = self.nodo.vecinos[direccion]
            self.posicion = (self.nodo.posicion + self.blanco.posicion) / 2.0

    def set_posicion(self):
        """Establece la posición de la entidad en el nodo actual."""
        self.posicion = self.nodo.posicion.copiar()
        # Redondear a 2 decimales para evitar errores de punto flotante
        self.posicion.x = round(self.posicion.x, 2)
        self.posicion.y = round(self.posicion.y, 2)

    def actualizar(self, dt):
        """Actualiza la posición y estado de la entidad."""
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

    def obtener_direcciones_validas(self):
        """Obtiene todas las direcciones válidas desde el nodo actual."""
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

    def validar_direccion(self, direccion):
        """Verifica si una dirección es válida desde el nodo actual."""
        if direccion is not STOP:
            if self.nodo.vecinos[direccion] is not None:
                return True
        return False

    def get_nuevo_blanco(self, direccion):
        """Obtiene el siguiente nodo blanco basado en la dirección."""
        if self.validar_direccion(direccion):
            return self.nodo.vecinos[direccion]
        return self.nodo

    def blanco_sobrepasado(self):
        if self.blanco is not None:
            vec1 = self.blanco.posicion - self.nodo.posicion
            vec2 = self.posicion - self.nodo.posicion
            nodo2_blanco = vec1.magnitudCuadrada()
            nodo2_self = vec2.magnitudCuadrada()

            # Añadir una condición especial para el nodo de la casa
            # if self.nodo.posicion.x == ANCHOCELDA * 12 and self.nodo.posicion.y == ALTURACELDA * 14:
               # return nodo2_self > nodo2_blanco + 1  # Añadir un margen extra

            return nodo2_self >= nodo2_blanco
        return False

    def direccion_reversa(self):
        """Invierte la dirección actual de la entidad."""
        self.direccion *= -1
        temp = self.nodo
        self.nodo = self.blanco
        self.blanco = temp

    def direccion_opuesta(self, direccion):
        """Verifica si una dirección es opuesta a la dirección actual."""
        if direccion is not STOP:
            if direccion == self.direccion * -1:
                return True
        return False

    def set_velocidad(self, velocidad):
        """Establece la velocidad de la entidad."""
        self.velocidad = velocidad * ANCHOCELDA / 16

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

    def nodo_inicio(self,nodo):
        self.nodo=nodo
        self.blanco=nodo
        self.set_posicion()
