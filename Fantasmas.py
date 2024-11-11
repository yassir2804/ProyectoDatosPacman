import pygame
from Entidad import Entidad
from Vector import Vector1
from Modo import Controladora_Modos
from Constantes import *


class Fantasma(Entidad):
    """
       Clase base para todos los fantasmas del juego Pacman.
       Maneja el comportamiento común de todos los fantasmas, incluyendo movimiento,
       modos de juego (Chase, Scatter, Freight), animaciones y sonidos.
       Hereda de la clase Entidad.
       """
    def __init__(self, nodo, pacman=None, blinky=None):
        super().__init__(nodo)
        self.nombre = FANTASMA
        self.puntos = 200
        self.pacman = pacman
        self.blinky = blinky
        self.modo = Controladora_Modos(self)
        self.nodoSpawn = nodo

        # Velocidad base y actual
        self.velocidad_base = 100  # Velocidad inicial
        self.set_velocidad(self.velocidad_base)

        self.direccion = DERECHA

        # Atributos del modo freight
        self.tiempo_freight = 0
        self.intervalo_freight = 0.2
        self.indice_freight = 0
        self.duracion_freight = 7
        self.parpadeo_freight = False
        self.contador_parpadeo = 0

        self.estado_salida = "esperando"
        self.posicion_salida = None

        # Sonidos
        self.sonido_freightmode = pygame.mixer.Sound("multimedia/scaredsonido1.wav")
        self.sonido_freightmode.set_volume(0.2)
        self.sonidoFreightSonando = False

        # Configuración de animaciones
        self.cargar_animaciones()
        self.cargar_animaciones_freight()
        self.cargar_animaciones_ojos()
        self.skin_inicial = self.skins[DERECHA][0]
        self.skin = self.skin_inicial

    def reset(self):
        super().reset()

    def cargar_animaciones_freight(self):
        self.skins_freight = [
            pygame.image.load("multimedia/FreightAzul.png").convert_alpha(),
            pygame.image.load("multimedia/FreightBlanco.png").convert_alpha()
        ]

    def cargar_animaciones_ojos(self):
        """Actualiza el skin del fantasmas mientras este en modo inactivo """
        self.skins_ojos = {
            ARRIBA: pygame.image.load("multimedia/OjosArriba.png").convert_alpha(),
            ABAJO: pygame.image.load("multimedia/OjosAbajo.png").convert_alpha(),
            IZQUIERDA: pygame.image.load("multimedia/OjosIzquierda.png").convert_alpha(),
            DERECHA: pygame.image.load("multimedia/OjosDerecha.png").convert_alpha()
        }

    def actualizar_skin_freight(self, dt):
        """Actualiza el skin durante el modo freight"""
        self.tiempo_freight += dt

        # Calcular el tiempo restante del modo freight
        tiempo_restante = self.duracion_freight - self.tiempo_freight

        # Si quedan 3 segundos o menos, activar el parpadeo
        if tiempo_restante <= 3:
            # Incrementar el contador de parpadeo
            self.contador_parpadeo += dt

            # Si se alcanzó el intervalo de parpadeo, cambiar el skin
            if self.contador_parpadeo >= self.intervalo_freight:
                # Reiniciar el contador de parpadeo
                self.contador_parpadeo = 0

                # Avanzar al siguiente skin en el ciclo de parpadeo
                self.indice_freight = (self.indice_freight + 1) % len(self.skins_freight)

                # Actualizar el skin actual
                self.skin = self.skins_freight[self.indice_freight]
        else:
            # Si aún queda bastante tiempo, mantener el skin normal de freight
            self.skin = self.skins_freight[0]
            self.contador_parpadeo = 0

    def actualizar(self, dt):
        """Actualiza el estado del fantasma"""
        self.modo.actualizar(dt)
        self._actualizar_modo_actual()
        self._actualizar_sonidos_y_sprites(dt)
        super().actualizar(dt)

    def _actualizar_modo_actual(self):
        """Actualiza el comportamiento según el modo actual"""
        if self.modo.current == SCATTER:
            self.scatter()
        elif self.modo.current == CHASE:
            self.chase()
        elif self.modo.current == SPAWN:
            self.spawn()

    def _actualizar_sonidos_y_sprites(self, dt):
        """Actualiza sonidos y sprites según el modo actual"""
        if self.modo.current == FREIGHT:
            self._manejar_modo_freight(dt)
        elif self.modo.current == SPAWN:
            self._manejar_modo_spawn()
        else:
            self._manejar_modo_normal(dt)

    def _manejar_modo_freight(self, dt):
        """Maneja la actualización en modo freight"""
        if not self.sonidoFreightSonando:
            self.sonido_freightmode.play(-1)
            self.sonidoFreightSonando = True
        self._actualizar_skin_freight(dt)

    def actualizar_velocidad_nivel(self, nivel):
        """Actualiza la velocidad base según el nivel"""
        # Aumenta la velocidad un 10% por nivel
        factor = 1 + (nivel - 1) * 0.1
        self.velocidad_base = 100 * factor * ANCHOCELDA / 16
        self.set_velocidad(self.velocidad_base)

    def _manejar_modo_spawn(self):
        """Maneja la actualización en modo spawn"""
        self.sonidoFreightSonando = False
        self.sonido_freightmode.stop()
        if hasattr(self, 'direccion') and self.direccion in self.skins_ojos:
            self.skin = self.skins_ojos[self.direccion]
        if self.posicion == self.meta:
            self.modo_normal()

    def _manejar_modo_normal(self, dt):
        """Maneja la actualización en modo normal"""
        self.sonidoFreightSonando = False
        self.sonido_freightmode.stop()
        self.actualizar_animacion(dt)

    def _actualizar_skin_freight(self, dt):
        """Actualiza el skin durante el modo freight"""
        self.tiempo_freight += dt
        tiempo_restante = self.duracion_freight - self.tiempo_freight

        if tiempo_restante <= 3:
            self._actualizar_parpadeo_freight(dt)
        else:
            self.skin = self.skins_freight[0]
            self.contador_parpadeo = 0

    def _actualizar_parpadeo_freight(self, dt):
        """Actualiza el parpadeo durante el modo freight"""
        self.contador_parpadeo += dt
        if self.contador_parpadeo >= self.intervalo_freight:
            self.contador_parpadeo = 0
            self.indice_freight = (self.indice_freight + 1) % len(self.skins_freight)
            self.skin = self.skins_freight[self.indice_freight]

    def chase(self):
        self.meta = Vector1(0, 0)

    def scatter(self):
        self.meta = Vector1(0, 0)

    def spawn(self):
        """Comportamiento de spawn común"""
        if hasattr(self, 'nodoSpawn') and self.nodoSpawn is not None:
            self.meta = self.nodoSpawn.posicion
        else:
            self.meta = self.nodo_inicio.posicion

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
            self.metodo_direccion = self.direccion_meta
            self.spawn()

    def modo_Freight(self):

            self.modo.modo_freight()
            if self.modo.current == FREIGHT:
                self.set_velocidad(50)
                self.metodo_direccion = self.direccion_aleatoria
                self.tiempo_freight = 0
                self.duracion_freight = 7
                self.puntos=200
                self.tiempo_parpadeo = 0
                self.skin = self.skins_freight[0]

    def modo_normal(self):
        # Establece la velocidad del personaje/enemigo a su velocidad base predeterminada
        self.set_velocidad(self.velocidad_base)

        # Configura el meto do de dirección para usar el sistema de búsqueda de objetivo/meta
        self.metodo_direccion = self.direccion_meta

        # Cambia el modo actual a CHASE (persecución)
        self.modo.current = CHASE

        # Impide que el personaje/enemigo pueda moverse hacia ABAJO desde el nodo de spawn
        self.nodoSpawn.denegar_acceso(ABAJO, self)

        # Si el objeto tiene un atributo 'direccion' y existe una skin asociada a esa dirección
        # actualiza la skin actual usando el primer sprite de la animación para esa dirección
        if hasattr(self, 'direccion') and self.direccion in self.skins:
            self.skin = self.skins[self.direccion][0]

    def cargar_animaciones(self):
        pass

    def actualizar_puntos(self):
        """Duplica los puntos del siguiente fantasma que será comido"""
        for fantasma in self:
            if fantasma.modo.current == FREIGHT:
                fantasma.puntos *= 2

    def render(self, pantalla):
        if self.visible:
            if self.skin:
                p = self.posicion.entero()
                rect = self.skin.get_rect(center=p)
                pantalla.blit(self.skin, rect)



class Blinky(Fantasma):
    """Fantasma rojo que persigue directamente a Pac-Man"""
    def __init__(self, nodo, pacman=None):
        super().__init__(nodo, pacman)
        self.nombre = BLINKY
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
    """Fantasma rosa que intenta emboscar a Pac-Man"""
    def __init__(self, nodo, pacman=None):
        super().__init__(nodo, pacman)
        self.nombre = PINKY
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(ANCHOCELDA * COLUMNAS, 0)

    def chase(self):
        self.meta = self.pacman.posicion + self.pacman.direcciones[self.pacman.direccion] * ANCHOCELDA * 4

    def reset(self):
        super().reset()

    def cargar_animaciones(self):
        self.skins = {
            ARRIBA: [pygame.image.load("multimedia/PinkyArr.png").convert_alpha()],
            ABAJO: [pygame.image.load("multimedia/PinkyAba.png").convert_alpha()],
            IZQUIERDA: [pygame.image.load("multimedia/PinkyIzq.png").convert_alpha()],
            DERECHA: [pygame.image.load("multimedia/PinkyDer.png").convert_alpha()]
        }


class Inky(Fantasma):
    """Fantasma azul que utiliza la posición de Blinky para calcular su objetivo"""
    def __init__(self, nodo, pacman=None, blinky=None):
        super().__init__(nodo, pacman, blinky)
        self.nombre = INKY
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(ANCHOCELDA * COLUMNAS, ALTURACELDA * FILAS)

    def chase(self):
        if self.blinky is None or not hasattr(self.blinky, 'posicion'):
            self.meta = self.pacman.posicion
            return

        vec1 = self.pacman.posicion + self.pacman.direcciones[self.pacman.direccion] * ANCHOCELDA * 2
        try:
            vec2 = (vec1 - self.blinky.posicion) * 2
            self.meta = self.blinky.posicion + vec2
        except Exception:
            self.meta = self.pacman.posicion

    def reset(self):
        super().reset()

    def cargar_animaciones(self):
        self.skins = {
            ARRIBA: [pygame.image.load("multimedia/InkyArr.png").convert_alpha()],
            ABAJO: [pygame.image.load("multimedia/InkyAba.png").convert_alpha()],
            IZQUIERDA: [pygame.image.load("multimedia/InkyIzq.png").convert_alpha()],
            DERECHA: [pygame.image.load("multimedia/InkyDer.png").convert_alpha()]
        }


class Clyde(Fantasma):
    """Fantasma naranja que alterna entre perseguir y huir de Pac-Man"""
    def __init__(self, nodo, pacman=None):
        super().__init__(nodo, pacman)
        self.nombre = CLYDE
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(0, ANCHOCELDA * FILAS)

    def chase(self):
        d = self.pacman.posicion - self.posicion
        ds = d.magnitudCuadrada()

        if ds <= (ANCHOCELDA * 8) ** 2:
            self.scatter()
        else:
            self.meta = self.pacman.posicion

    def reset(self):
        super().reset()

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
        self.tiempo_entre_fantasmas = 5
        self.fantasmas_liberados = 0
        self.orden_fantasmas = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.fantasmas)

    def actualizar_velocidades_nivel(self, nivel):
        """Actualiza las velocidades de todos los fantasmas según el nivel"""
        for fantasma in self.fantasmas:
            fantasma.actualizar_velocidad_nivel(nivel)

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
        for fantasma in self.fantasmas:
            fantasma.reset()

    def esconder(self):
        for fantasma in self:
            fantasma.visible = False

    def mostrar(self):
        for fantasma in self:
            fantasma.visible = True

    def modo_freight_activo(self):
        return any(fantasma.modo.current == FREIGHT for fantasma in [self.blinky, self.pinky, self.inky, self.clyde])

    def render(self, pantalla):
        for fantasma in self:
            fantasma.render(pantalla)