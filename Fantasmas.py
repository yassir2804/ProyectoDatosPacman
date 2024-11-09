

from Entidad import *
from Modo import Controladora_Modos
from Grafo import *


import pygame
from Entidad import Entidad
from Vector import Vector1
from Modo import Controladora_Modos
from Constantes import *

class Fantasma(Entidad):
    def __init__(self, nodo, pacman=None, blinky=None):
        super().__init__(nodo)
        self.nombre = FANTASMA
        self.puntos = 200
        self.meta = Vector1(0, 0)
        self.pacman = pacman
        self.modo = Controladora_Modos(self)
        self.blinky = blinky
        self.nodoSpawn = nodo # Ensure initial position is set


        self.cargar_animaciones()
        self.cargar_animaciones_freight()
        self.cargar_animaciones_ojos()
        self.skin_inicial = self.skins[DERECHA][0]
        self.skin = self.skin_inicial
        self.tiempo_freight = 0
        self.intervalo_freight = 0.2
        self.indice_freight = 0
        self.estado_salida = "esperando"
        self.posicion_salida = None

        self.duracion_freight = 7
        self.parpadeo_freight = False
        self.contador_parpadeo = 0
        self.velocidad = 100
        self.direccion = DERECHA

        self.sonido_freightmode = pygame.mixer.Sound("multimedia/scaredsonido1.wav")
        self.sonido_freightmode.set_volume(0.2)
        self.sonidoFreightSonando = False

    def reset(self):
        """Reinicia el fantasma a su estado inicial"""
        # Reset de la entidad padre
        super().reset()
        # Reset de atributos básicos
        self.puntos = 200
        self.metodo_direccion = self.direccion_meta

    def cargar_animaciones_freight(self):
        self.skins_freight = [
            pygame.image.load("multimedia/FreightAzul.png").convert_alpha(),
            pygame.image.load("multimedia/FreightBlanco.png").convert_alpha()
        ]


    def cargar_animaciones_ojos(self):
        self.skins_ojos = {
            ARRIBA: pygame.image.load("multimedia/OjosArriba.png").convert_alpha(),
            ABAJO: pygame.image.load("multimedia/OjosAbajo.png").convert_alpha(),
            IZQUIERDA: pygame.image.load("multimedia/OjosIzquierda.png").convert_alpha(),
            DERECHA: pygame.image.load("multimedia/OjosDerecha.png").convert_alpha()
        }

    def actualizar_skin_freight(self, dt):
        self.tiempo_freight += dt
        tiempo_restante = self.duracion_freight - self.tiempo_freight

        if tiempo_restante <= 3:
            self.contador_parpadeo += dt
            if self.contador_parpadeo >= self.intervalo_freight:
                self.contador_parpadeo = 0
                self.indice_freight = (self.indice_freight + 1) % len(self.skins_freight)
                self.skin = self.skins_freight[self.indice_freight]
        else:
            self.skin = self.skins_freight[0]
            self.contador_parpadeo = 0

    def actualizar(self, dt):

        self.modo.actualizar(dt)
        if self.modo.current == SCATTER:
            self.scatter()
        elif self.modo.current == CHASE:
            self.chase()
        elif self.modo.current == SPAWN:
            self.spawn()

        if self.modo.current == FREIGHT:
            if not self.sonidoFreightSonando:  # Check if the sound is already playing
                self.sonido_freightmode.play(-1)  # Start playing the sound in loop
                self.sonidoFreightSonando = True  # Set the flag to indicate the sound is playing
            self.actualizar_skin_freight(dt)
        elif self.modo.current == SPAWN:
            self.sonidoFreightSonando = False  # Reset the flag when exiting FREIGHT mode
            self.sonido_freightmode.stop()  # Stop the freight sound
            if hasattr(self, 'direccion') and self.direccion in self.skins_ojos:
                self.skin = self.skins_ojos[self.direccion]
            if self.posicion == self.meta:
                self.modo_normal()
        else:
            self.sonidoFreightSonando = False  # Reset the flag when in any other mode
            self.sonido_freightmode.stop()  # Ensure the freight sound stops
            self.actualizar_animacion(dt)

        # Ensure self.direccion is valid before calling super().actualizar(dt)
        if self.direccion not in self.direcciones:
            self.direccion = DERECHA  # Default to a valid direction

        super().actualizar(dt)

    def chase(self):
        self.meta = Vector1(0, 0)

    def scatter(self):
        self.meta = Vector1(0, 0)

    def spawn(self):
        if hasattr(self, 'nodoSpawn') and self.nodoSpawn is not None:
            self.meta = self.nodoSpawn.posicion
        else:
            self.meta = self.nodoInicial.posicion

    def setSpawnNode(self, nodo):
        self.nodoSpawn = nodo

    def iniciar_spawn(self):
        """Inicia el modo spawn cuando el fantasma es comido"""

        self.modo.set_modo_spawn()
        self.set_velocidad(300)
        self.metodo_direccion = self.direccion_meta
        self.spawn()
        # No resetear la skin aquí, ya que queremos mantener los ojos

        # self.modo.set_modo_spawn()
        if self.modo.current == SPAWN:
            self.set_velocidad(150)
            self.metodo_direccion = self.direccion_meta
            self.spawn()

    def modo_Freight(self):
            self.modo.modo_freight()
            if self.modo.current == FREIGHT:
                self.set_velocidad(50)
                self.metodo_direccion = self.direccion_aleatoria
                self.tiempo_freight = 0
                self.duracion_freight = 7
                self.tiempo_parpadeo = 0
                self.skin = self.skins_freight[0]

    def modo_normal(self):
        self.set_velocidad(100)
        self.metodo_direccion = self.direccion_meta
        self.modo.current = CHASE
        self.nodoSpawn.denegar_acceso(ABAJO, self)
        if hasattr(self, 'direccion') and self.direccion in self.skins:
            self.skin = self.skins[self.direccion][0]

    def cargar_animaciones(self):
        pass

    def render(self, pantalla):
        if self.visible:
            if self.skin:
                p = self.posicion.entero()
                rect = self.skin.get_rect(center=p)
                pantalla.blit(self.skin, rect)
            else:
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

    def reset(self):
        super().reset()


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

    def reset(self):
        super().reset()
        self.velocidad = 100 * ANCHOCELDA / 16


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

    def reset(self):
        super().reset()
        self.velocidad = 100 * ANCHOCELDA / 16

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

    def reset(self):
        super().reset()
        self.velocidad = 100 * ANCHOCELDA / 16


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
        self.tiempo_transcurrido = 0
        self.tiempo_entre_fantasmas = 5  # segundos entre cada fantasma
        self.fantasmas_liberados = 0
        self.orden_fantasmas = [self.blinky, self.pinky, self.inky, self.clyde]


    def __iter__(self):
        return iter(self.fantasmas)

    def actualizar(self, dt):
        for fantasma in self.fantasmas:
            fantasma.actualizar(dt)

    def modo_Freight(self):
        for fantasma in self:
            fantasma.modo_Freight()
        self.resetear_puntos()

    def modo_Chase(self):
        for fantasma in self:
            fantasma.modo_normal()

    def set_nodo_spawn(self, nodo):
        for fantasma in self:
            fantasma.setSpawnNode(nodo)

    def actualizarPuntos(self):
        for fantasma in self:
            fantasma.puntos *= 2

    def resetear_puntos(self):
        for fantasma in self:
            fantasma.puntos = 200

    def reset(self):
        """Reset all ghosts to their initial positions"""
        for fantasma in self.fantasmas:
            fantasma.reset()


    def esconder(self):
        for fantasma in self:
            fantasma.visible = False

    def mostrar(self):
        for fantasma in self:
            fantasma.visible = True

    def render(self, pantalla):
        for fantasma in self:
            fantasma.render(pantalla)