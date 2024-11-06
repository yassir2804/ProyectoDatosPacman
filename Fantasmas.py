

from Pacman import *

from numpy.random import random
from Constantes import *
from Entidad import *
from Modo import Controladora_Modos
from Grafo import *

from random import choice
import pygame


class Fantasma(Entidad):
    def __init__(self, nodo, pacman=None, blinky=None):
        super().__init__(nodo)
        self.nombre = FANTASMA
        self.puntos = 200
        self.meta = Vector1(0, 0)
        self.pacman = pacman
        self.modo = Controladora_Modos(self)
        self.blinky = blinky
        self.nodoInicial = nodo
        self.metodo_direccion = self.direccion_meta
        # Activación para salir de casa fantasmas

        self.activo = False
        self.en_casa = True  #Conocer si el fantasma se encuentra en la casa
        self.posicion_inicial = nodo.posicion.copiar()

        self.movimiento_casa = ARRIBA
        self.velocidad_casa = 50

        # Los límites se establecerán desde GrupoFantasmas
        self.limite_izquierdo = 0
        self.limite_derecho = 0
        self.limite_arriba = 0
        self.limite_abajo = 0

        # Inicialización de la animación
        self.cargar_animaciones()
        self.cargar_animaciones_freight()
        self.skin = self.skins[DERECHA][0]  # Imagen inicial
        self.tiempo_freight = 0
        self.intervalo_freight = 0.2  # Cambiar cada 0.2 segundos
        self.indice_freight = 0

    def reset(self):
        self.puntos = 200
        self.metodo_direccion = self.direccion_meta
        self.nodo_inicio(self.nodoInicial)
        self.activo = False
        self.en_casa = True  # Resetear estado de casa
        self.posicion = self.posicion_inicial.copiar()
        self.modo_normal()  # Asegurar que esté en modo normal al resetear

    def cargar_animaciones_freight(self):
        # Cargar las imágenes de freight una sola vez
        self.skins_freight = [
            pygame.image.load("multimedia/FreightAzul.png").convert_alpha(),
            pygame.image.load("multimedia/FreightBlanco.png").convert_alpha()
        ]

    def mover_en_casa(self, dt):
        """Método para mover el fantasma dentro de la casa"""
        if not self.en_casa:
            return

        # Movimiento vertical
        if self.movimiento_casa == 'arriba':
            self.posicion.y -= self.velocidad_casa * dt
            if self.posicion.y <= self.limite_arriba:
                self.posicion.y = self.limite_arriba
                self.movimiento_casa = 'abajo'
        else:
            self.posicion.y += self.velocidad_casa * dt
            if self.posicion.y >= self.limite_abajo:
                self.posicion.y = self.limite_abajo
                self.movimiento_casa = 'arriba'

        # Mantener dentro de límites horizontales
        self.posicion.x = max(self.limite_izquierdo,
                              min(self.posicion.x, self.limite_derecho))
    def liberar_de_casa(self):
        """Método para liberar al fantasma de la casa inicial"""
        self.activo = True
        self.en_casa = False
        self.modo_normal()  # Asegurar que empiece en modo normal

    def actualizar_skin_freight(self, dt):
        self.tiempo_freight += dt
        if self.tiempo_freight >= self.intervalo_freight:
            self.tiempo_freight = 0
            self.indice_freight = (self.indice_freight + 1) % len(self.skins_freight)
            self.skin = self.skins_freight[self.indice_freight]

    def actualizar(self, dt):
        if not self.activo and self.en_casa:
            self.mover_en_casa(dt)
            return

        self.modo.actualizar(dt)
        if self.modo.current == SCATTER:
            self.scatter()
        elif self.modo.current == CHASE:
            self.chase()

        # Actualizar animación según el modo
        if self.modo.current == FREIGHT:
            self.actualizar_skin_freight(dt)
        else:
            self.actualizar_animacion(dt)

        super().actualizar(dt)


    def chase(self):
        self.meta = self.pacman.posicion

    def scatter(self):
        self.meta = Vector1(0, 0)

    def spawn(self):
        self.meta = self.nodoSpawn.posicion

    def setSpawnNode(self, nodo):
        self.nodoSpawn = nodo

    def iniciar_spawn(self):
        self.modo.set_modo_spawn()
        if self.modo.current == SPAWN:
            self.set_velocidad(150)
            self.metodo_direccion = self.direccion_meta
            self.spawn()

    def modo_Freight(self):
        """Solo entrar en modo freight si no está en casa"""
        if not self.en_casa:
            self.modo.modo_freight()
            if self.modo.current == FREIGHT:
                self.set_velocidad(50)
                self.metodo_direccion = self.direccion_aleatoria
                self.tiempo_freight = 0
                self.indice_freight = 0

    def modo_normal(self):
        self.set_velocidad(100)
        #self.modo.modo_chase()
        self.metodo_direccion = self.direccion_meta

    def cargar_animaciones(self):
        """Método base para cargar animaciones de fantasmas"""
        pass

    def render(self, pantalla):
        """Renderiza el fantasma en la pantalla"""
        if self.visible:
            if self.skin:
                # Obtener la posición como tupla de enteros
                p = self.posicion.entero()
                # Obtener el rectángulo de la imagen centrado en la posición actual
                rect = self.skin.get_rect(center=p)
                # Dibujar la imagen actual de la animación
                pantalla.blit(self.skin, rect)
            else:
                # Fallback al círculo original si no hay skin
                p = self.posicion.entero()
                pygame.draw.circle(pantalla, self.color, p, self.radio)


class Blinky(Fantasma):
    def __init__(self, nodo, pacman=None):
        super().__init__(nodo, pacman)

        self.nombre = BLINKY
        self.color = ROJO
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(0, 0)

    def chase(self):
        self.meta = self.pacman.posicion

    def cargar_animaciones(self):
        self.skins = {
            ARRIBA: [pygame.image.load("multimedia/BlinkyArr.png").convert_alpha()],
            ABAJO: [pygame.image.load("multimedia/BlinkyAba.png").convert_alpha()],
            IZQUIERDA: [pygame.image.load("multimedia/BlinkyIzq.png").convert_alpha()],
            DERECHA: [pygame.image.load("multimedia/BlinkyDer.png").convert_alpha()]
        }


class Pinky(Fantasma):
    def __init__(self, nodo, pacman=None):
        super().__init__(nodo, pacman)
        self.nombre = PINKY
        self.color = ROSADO
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(ANCHOCELDA * COLUMNAS, 0)

    def chase(self):
        # Pinky aims 4 tiles ahead of Pacman's current direction
        self.meta = self.pacman.posicion + self.pacman.direcciones[self.pacman.direccion] * ANCHOCELDA * 4

    def cargar_animaciones(self):
        self.skins = {
            ARRIBA: [pygame.image.load("multimedia/PinkyArr.png").convert_alpha()],
            ABAJO: [pygame.image.load("multimedia/PinkyAba.png").convert_alpha()],
            IZQUIERDA: [pygame.image.load("multimedia/PinkyIzq.png").convert_alpha()],
            DERECHA: [pygame.image.load("multimedia/PinkyDer.png").convert_alpha()]
        }


class Inky(Fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        super().__init__(nodo, pacman, blinky)
        self.nombre = INKY
        self.color = CELESTE
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(ANCHOCELDA * COLUMNAS, ALTURACELDA * FILAS)

    def chase(self):
        if self.blinky is None or not hasattr(self.blinky, 'posicion'):
            self.meta = self.pacman.posicion
            return

        # First, get the position 2 tiles ahead of Pacman
        vec1 = self.pacman.posicion + self.pacman.direcciones[self.pacman.direccion] * ANCHOCELDA * 2
        # Then, get the vector from Blinky to that position and double it
        try:
            vec2 = (vec1 - self.blinky.posicion) * 2
            self.meta = self.blinky.posicion + vec2
        except Exception:
            # Si hay algún error en el cálculo, perseguir directamente a Pacman
            self.meta = self.pacman.posicion

    def cargar_animaciones(self):
        self.skins = {
            ARRIBA: [pygame.image.load("multimedia/InkyArr.png").convert_alpha()],
            ABAJO: [pygame.image.load("multimedia/InkyAba.png").convert_alpha()],
            IZQUIERDA: [pygame.image.load("multimedia/InkyIzq.png").convert_alpha()],
            DERECHA: [pygame.image.load("multimedia/InkyDer.png").convert_alpha()]
        }


class Clyde(Fantasma):
    def __init__(self, nodo, pacman=None):
        super().__init__(nodo, pacman)
        self.nombre = CLYDE
        self.color = NARANJA
        self.velocidad = 100 * ANCHOCELDA / 16
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(0, ANCHOCELDA * FILAS)

    def chase(self):

        # Calculate distance to Pacman
        d = self.pacman.posicion - self.posicion
        ds = d.magnitudCuadrada()

        # If Clyde is closer than 8 tiles to Pacman, go to scatter mode
        if ds <= (ANCHOCELDA * 8) ** 2:
            self.scatter()
        else:
            # Otherwise chase Pacman like Blinky
            self.meta = self.pacman.posicion

    def cargar_animaciones(self):
        self.skins = {
            ARRIBA: [pygame.image.load("multimedia/ClydeArr.png").convert_alpha()],
            ABAJO: [pygame.image.load("multimedia/ClydeAba.png").convert_alpha()],
            IZQUIERDA: [pygame.image.load("multimedia/ClydeIzq.png").convert_alpha()],
            DERECHA: [pygame.image.load("multimedia/ClydeDer.png").convert_alpha()]
        }


class GrupoFantasmas(object):
    def __init__(self, nodo, pacman):
        self.blinky = Blinky(nodo, pacman)
        self.pinky = Pinky(nodo, pacman)
        self.inky = Inky(nodo, pacman, self.blinky)
        self.clyde = Clyde(nodo, pacman)
        self.fantasmas = [self.blinky, self.pinky, self.inky, self.clyde]
        # Activar solo a Blinky inicialmente
        self.blinky.activo = True
        # Calcular límites de la casa basados en las posiciones iniciales
        self.calcular_limites_casa()

    def __iter__(self):
        return iter(self.fantasmas)

    def actualizar(self, dt):
        for fantasma in self:
            fantasma.actualizar(dt)

    def modo_Freight(self):
        for fantasma in self:
            fantasma.modo_Freight()
        self.resetearPuntos()

    def modo_Chase(self):
        for fantasma in self:
            fantasma.modo_normal()

    def setSpawnNode(self, nodo):
        for fantasma in self:
            fantasma.setSpawnNode(nodo)

    def actualizarPuntos(self):
        for fantasma in self:
            fantasma.puntos *= 2

    def resetearPuntos(self):
        for fantasma in self:
            fantasma.puntos = 200

    def reset(self):
        for fantasma in self:
            fantasma.reset()
            # Reactivar solo a Blinky
            self.blinky.activo = True

    def esconder(self):
        for fantasma in self:
            fantasma.visible = False

    def activar_fantasma(self, fantasma):
        """Activa un fantasma específico"""
        fantasma.activo = True
        fantasma.modo_normal()  # Asegurar que empiece en modo normal

    def calcular_limites_casa(self):
        """Calcula los límites de la casa basados en las posiciones de los fantasmas"""
        posiciones_x = [fantasma.posicion_inicial.x for fantasma in self.fantasmas]
        posiciones_y = [fantasma.posicion_inicial.y for fantasma in self.fantasmas]

        # Añadir un margen de movimiento
        margen = ALTURACELDA * 2  # Ajusta este valor según necesites

        # Calcular límites
        limite_izquierda = min(posiciones_x) - ANCHOCELDA
        limite_derecha = max(posiciones_x) + ANCHOCELDA
        limite_arriba = min(posiciones_y) - margen / 2
        limite_abajo = max(posiciones_y) + margen / 2

        # Asignar límites a cada fantasma
        for fantasma in self.fantasmas:
            fantasma.limite_izquierdo = limite_izquierda
            fantasma.limite_derecho = limite_derecha
            fantasma.limite_arriba = limite_arriba
            fantasma.limite_abajo = limite_abajo
    def desactivar_todos(self):
        """Desactiva todos los fantasmas excepto Blinky"""
        for fantasma in self.fantasmas[1:]:  # Todos excepto Blinky
            fantasma.activo = False
            fantasma.posicion = fantasma.posicion_inicial.copiar()

    def mostrar(self):
        for fantasma in self:
            fantasma.visible = True

    def render(self, pantalla):
        for fantasma in self:
            fantasma.render(pantalla)
