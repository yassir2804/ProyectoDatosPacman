import pygame
from Entidad import Entidad
from Vector import Vector1
from Modo import Controladora_Modos
from Constantes import *


class Fantasma(Entidad):
    """
        Clase que representa a los fantasmas en el juego de Pac-Man.
        Hereda de la clase Entidad y gestiona la logica específica del comportamiento
        de los fantasmas, incluyendo los modos de movimiento (normal y Freight),
        la interaccion con Pac-Man, y las animaciones correspondientes.
    """
    def __init__(self, nodo, pacman=None, blinky=None):
        # Inicializa la entidad, en este caso un fantasma, con su nodo de inicio
        super().__init__(nodo)  # Llama al constructor de la clase base
        self.nombre = FANTASMA  # Nombre de la entidad
        self.puntos = 200  # Puntos que da el fantasma cuando es comido
        self.meta = Vector1(0, 0)  # Inicializa la meta del fantasma
        self.pacman = pacman  # Referencia al personaje Pacman
        self.blinky = blinky  # Referencia al fantasma Blinky
        self.modo = Controladora_Modos(self)  # Controla el modo del fantasma
        self.nodoSpawn = nodo  # Nodo donde el fantasma aparece inicialmente

        # Velocidad base y actual del fantasma
        self.velocidad_base = 100  # Velocidad inicial
        self.set_velocidad(self.velocidad_base)  # Establece la velocidad inicial
        self.direccion = DERECHA  # Dirección inicial del movimiento del fantasma

        # Atributos específicos para el modo "freight" (cuando el fantasma esta asustado)
        self.tiempo_freight = 0  # Tiempo que ha pasado en el modo freight
        self.intervalo_freight = 0.2  # Intervalo entre parpadeos en el modo freight
        self.indice_freight = 0  # Indice para las animaciones en modo freight
        self.duracion_freight = 7  # Duracion total del modo freight
        self.parpadeo_freight = False  # Controla si el fantasma debe parpadear en freight
        self.contador_parpadeo = 0  # Cuenta los parpadeos en freight

        self.estado_salida = "esperando"  # Estado de espera para salir del modo freight
        self.posicion_salida = None  # Posicion de salida del modo freight

        # Sonidos utilizados en el modo freight
        self.sonido_freightmode = pygame.mixer.Sound("multimedia/scaredsonido1.wav")  # Carga el sonido
        self.sonido_freightmode.set_volume(0.2)  # Ajusta el volumen del sonido
        self.sonidoFreightSonando = False  # Flag para saber si el sonido está sonando

        # Configuracion de las animaciones
        self.cargar_animaciones()  # Carga las animaciones normales del fantasma
        self.cargar_animaciones_freight()  # Carga las animaciones para el modo freight
        self.cargar_animaciones_ojos()  # Carga las animaciones de los ojos del fantasma
        self.skin_inicial = self.skins[DERECHA][0]  # Establece el skin inicial del fantasma mirando a la derecha
        self.skin = self.skin_inicial  # Asigna el skin inicial

    def reset(self):
        super().reset()

    def cargar_animaciones_freight(self):
        # Cargar las dos fotos del fantasma en freight mode
        self.skins_freight = [
            pygame.image.load("multimedia/FreightAzul.png").convert_alpha(),
            pygame.image.load("multimedia/FreightBlanco.png").convert_alpha()
        ]


    def cargar_animaciones_ojos(self):
        # Actualiza la skin de los fantasmas cuando se lo hayan comido
        self.skins_ojos = {
            ARRIBA: pygame.image.load("multimedia/OjosArriba.png").convert_alpha(),
            ABAJO: pygame.image.load("multimedia/OjosAbajo.png").convert_alpha(),
            IZQUIERDA: pygame.image.load("multimedia/OjosIzquierda.png").convert_alpha(),
            DERECHA: pygame.image.load("multimedia/OjosDerecha.png").convert_alpha()
        }

    def actualizar_skin_freight(self, dt):
        # Actualiza la skin en el modo freight, se hace la logica tambien de que cuando el tiempo sea
        # menor a 3, empiece a cambiar las imagenes rapido para indicar que esta por acabar el tiempo
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
        # Actualiza los fantasmas
        self.modo.actualizar(dt)
        self._actualizar_modo_actual()
        self._actualizar_sonidos_y_sprites(dt)
        super().actualizar(dt)

    def _actualizar_modo_actual(self):
        # Dependiendo del modo del fantasma, en el current se settea su modo actual
        if self.modo.current == SCATTER:
            self.scatter()
        elif self.modo.current == CHASE:
            self.chase()
        elif self.modo.current == SPAWN:
            self.spawn()

    def _actualizar_sonidos_y_sprites(self, dt):
        # Actualiza los sonidos y los sprites del fantasma
        if self.modo.current == FREIGHT:
            self._manejar_modo_freight(dt)
        elif self.modo.current == SPAWN:
            self._manejar_modo_spawn()
        else:
            self._manejar_modo_normal(dt)

    def _manejar_modo_freight(self, dt):
        # Maneja la actualizacion en modo freight
        if not self.sonidoFreightSonando:
            self.sonido_freightmode.play(-1)
            self.sonidoFreightSonando = True
        self._actualizar_skin_freight(dt)

    def actualizar_velocidad_nivel(self, nivel):
        # actualiza la velocidad base segun nivel
        # Aumenta la velocidad un 10% por nivel
        factor = 1 + (nivel - 1) * 0.1
        self.velocidad_base = 100 * factor * ANCHOCELDA / 16
        self.set_velocidad(self.velocidad_base)

    def _manejar_modo_spawn(self):
        # se actualiza en modo spawn
        self.sonidoFreightSonando = False
        self.sonido_freightmode.stop()
        if hasattr(self, 'direccion') and self.direccion in self.skins_ojos:
            self.skin = self.skins_ojos[self.direccion]
        if self.posicion == self.meta:
            self.modo_normal()

    def _manejar_modo_normal(self, dt):
        # se actualiza en modo normal
        self.sonidoFreightSonando = False
        self.sonido_freightmode.stop()
        self.actualizar_animacion(dt)

    def _actualizar_skin_freight(self, dt):
        # se actualiza la skin del modo freighteeee
        self.tiempo_freight += dt
        tiempo_restante = self.duracion_freight - self.tiempo_freight

        if tiempo_restante <= 3:
            self._actualizar_parpadeo_freight(dt)
        else:
            self.skin = self.skins_freight[0]
            self.contador_parpadeo = 0

    def _actualizar_parpadeo_freight(self, dt):
        # actualiza el parpadeo de las skins
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
        # comportamiento del spawn del fantasma
        if hasattr(self, 'nodoSpawn') and self.nodoSpawn is not None:
            self.meta = self.nodoSpawn.posicion
        else:
            self.meta = self.nodoInicial.posicion

    def setSpawnNode(self, nodo):
        self.nodoSpawn = nodo

    def iniciar_spawn(self):
        """Inicia el modo spawn cuando el fantasma es comido"""
        # Inicia el modo spawn cuando el fantasma es comido
        self.modo.set_modo_spawn()
        self.set_velocidad(300)
        self.metodo_direccion = self.direccion_meta
        self.spawn()

        if self.modo.current == SPAWN:
            self.metodo_direccion = self.direccion_meta
            self.spawn()

    def modo_Freight(self):
        # Este metodo activa el modo Freight para el fantasma,
        #  cambiando su comportamiento, velocidad, direccion aleatoria y skin.
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
        # Este metodo activa el modo Normal para el fantasma,
        # cambiando su comportamiento, velocidad
        self.set_velocidad(self.velocidad_base)
        self.metodo_direccion = self.direccion_meta
        self.modo.current = CHASE
        self.nodoSpawn.denegar_acceso(ABAJO, self)
        if hasattr(self, 'direccion') and self.direccion in self.skins:
            self.skin = self.skins[self.direccion][0]

    def cargar_animaciones(self):
        pass

    def actualizarPuntos(self):
        # Duplica los puntos del siguiente fantasma que es comido
        for fantasma in self:
            if fantasma.modo.current == FREIGHT:
                fantasma.puntos *= 2

    def render(self, pantalla):
        # Se hace visual el fantasma
        if self.visible:
            if self.skin:
                p = self.posicion.entero()
                rect = self.skin.get_rect(center=p)
                pantalla.blit(self.skin, rect)
            else:
                p = self.posicion.entero()
                pygame.draw.circle(pantalla, self.color, p, self.radio)


class Blinky(Fantasma):
    """Fantasma rojo que persigue directamente a Pac-Man"""
    def __init__(self, nodo, pacman=None):
        super().__init__(nodo, pacman)
        self.nombre = BLINKY
        self.color = ROJO
        self.radio = 10
        self.radio_colision = 5


    def scatter(self):
        self.meta = Vector1(0, 0)

    def chase(self):
        self.meta = self.pacman.posicion

    def reset(self):
        super().reset()

    def cargar_animaciones(self):
        # Se cargan las animaciones de Blinky en las 4 direcciones
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
        self.color = ROSADO
        self.radio = 10
        self.radio_colision = 5

    def scatter(self):
        self.meta = Vector1(ANCHOCELDA * COLUMNAS, 0)

    def chase(self):
        self.meta = self.pacman.posicion + self.pacman.direcciones[self.pacman.direccion] * ANCHOCELDA * 4

    def reset(self):
        super().reset()


    def cargar_animaciones(self):
        # Se cargan las animaciones de Pinky en las 4 direcciones
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
        self.color = CELESTE
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
            # Si hay algun error en el cálculo, perseguir directamente a Pacman
            self.meta = self.pacman.posicion

    def reset(self):
        super().reset()

    def cargar_animaciones(self):
        # Se cargan las animaciones de Inky en las 4 direcciones
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
        self.color = NARANJA
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
        # Se cargan las animaciones de Clyde en las 4 direcciones
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
        """Reset all ghosts to their initial positions"""
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