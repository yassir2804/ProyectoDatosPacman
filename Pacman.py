import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *
from Entidad import Entidad


class Pacman(Entidad):
    def __init__(self, nodo):
        super().__init__(nodo)
        self.nombre = PACMAN
        self.color = AMARILLO
        self.velocidad = 75 * ANCHOCELDA / 16
        self.direccion_deseada = STOP
        self.tiene_poder = False
        self.tiempo_poder = 0
        self.duracion_poder = 7
        self.fantasmas = []

        # Cargar todas las imágenes de Pac-Man para cada dirección
        self.skins = {
            ARRIBA: [
                pygame.image.load("multimedia/1_Arr.png").convert_alpha(),
                pygame.image.load("multimedia/2_Arr.png").convert_alpha(),
                pygame.image.load("multimedia/3_Arr.png").convert_alpha(),
                pygame.image.load("multimedia/4_Arr.png").convert_alpha(),
                pygame.image.load("multimedia/5_Arr.png").convert_alpha(),
                pygame.image.load("multimedia/6_Arr.png").convert_alpha()
            ],
            ABAJO: [
                pygame.image.load("multimedia/1_Aba.png").convert_alpha(),
                pygame.image.load("multimedia/2_Aba.png").convert_alpha(),
                pygame.image.load("multimedia/3_Aba.png").convert_alpha(),
                pygame.image.load("multimedia/4_Aba.png").convert_alpha(),
                pygame.image.load("multimedia/5_Aba.png").convert_alpha(),
                pygame.image.load("multimedia/6_Aba.png").convert_alpha()
            ],
            IZQUIERDA: [
                pygame.image.load("multimedia/1_Izq.png").convert_alpha(),
                pygame.image.load("multimedia/2_Izq.png").convert_alpha(),
                pygame.image.load("multimedia/3_Izq.png").convert_alpha(),
                pygame.image.load("multimedia/4_Izq.png").convert_alpha(),
                pygame.image.load("multimedia/5_Izq.png").convert_alpha(),
                pygame.image.load("multimedia/6_Izq.png").convert_alpha()
            ],
            DERECHA: [
                pygame.image.load("multimedia/1_Der.png").convert_alpha(),
                pygame.image.load("multimedia/2_Der.png").convert_alpha(),
                pygame.image.load("multimedia/3_Der.png").convert_alpha(),
                pygame.image.load("multimedia/4_Der.png").convert_alpha(),
                pygame.image.load("multimedia/5_Der.png").convert_alpha(),
                pygame.image.load("multimedia/6_Der.png").convert_alpha()
            ]
        }

        # Escalar las imágenes al tamaño adecuado
        self.radio = ANCHOCELDA // 2
        for direccion in self.skins:
            for i in range(len(self.skins[direccion])):
                self.skins[direccion][i] = pygame.transform.scale(self.skins[direccion][i],
                                                                  (self.radio * 2, self.radio * 2))

        # Variables para la animación
        self.direccion = DERECHA
        self.skin_index = 0
        self.skin = self.skins[self.direccion][self.skin_index]

        # Timer de animación y velocidad de cambio de imagen
        self.animation_timer = 0
        self.animation_interval = 0.05  # Cambiar de imagen cada 0.1 segundos

    def establecer_fantasmas(self, fantasmas):
        self.fantasmas = fantasmas

    def activar_poder(self):
        self.tiene_poder = True
        self.tiempo_poder = self.duracion_poder
        for fantasma in self.fantasmas:
            fantasma.set_scatter_mode()

    def actualizar_poder(self, dt):
        if self.tiene_poder:
            self.tiempo_poder -= dt
            if self.tiempo_poder <= 0:
                self.tiene_poder = False
                self.tiempo_poder = 0
                for fantasma in self.fantasmas:
                    fantasma.modo = CHASE

    def actualizar(self, dt):
        """Actualiza la posición, el poder y la animación de Pacman en el tiempo `dt`."""
        self.actualizar_poder(dt)
        # Solo avanza si no está en STOP; de lo contrario, mantiene la posición pero sigue animando
        if self.direccion != STOP:
            self.posicion += self.direcciones[self.direccion] * self.velocidad * dt

        # Control del tiempo de animación
        self.animation_timer += dt
        if self.animation_timer >= self.animation_interval:
            self.animation_timer = 0
            self.actualizar_skin()  # Cambia al siguiente fotograma de la animación

        # Detectar la dirección del teclado y actualizar `direccion_deseada`
        direccion = self.entrada_teclado()
        if direccion != STOP:
            self.direccion_deseada = direccion

        # Actualizar dirección si se puede
        if self.blanco_sobrepasado():
            self.nodo = self.blanco

            if self.nodo.vecinos[PORTAL] is not None:
                self.nodo = self.nodo.vecinos[PORTAL]

            # Cambiar a la dirección deseada si es válida
            if self.direccion_deseada != STOP and self.validar_direccion(self.direccion_deseada):
                self.direccion = self.direccion_deseada
                self.skin_index = 0  # Reiniciar la animación de la nueva dirección
                self.skin = self.skins[self.direccion][self.skin_index]
                self.direccion_deseada = STOP

            # Actualizar el próximo objetivo de movimiento
            self.blanco = self.get_nuevo_blanco(self.direccion)

            if self.blanco is self.nodo:
                self.direccion = STOP  # Si no hay camino, detente, pero continúa animando

            # Actualizar la posición
            self.set_posicion()
        else:
            # Reversa la dirección si es opuesta y resetear la animación
            if self.direccion_opuesta(direccion):
                self.direccion_reversa()
                self.skin_index = 0
                self.skin = self.skins[self.direccion][self.skin_index]  # Cambiar la skin al revertir

    def render(self, pantalla):
        p = self.posicion.entero()
        rect = self.skin.get_rect(center=p)
        pantalla.blit(self.skin, rect)

        if self.tiene_poder:
            borde_superior = pygame.Surface((self.radio * 2 + 4, self.radio * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(borde_superior, AZUL + (100,), (self.radio + 2, self.radio + 2), self.radio + 2, 2)
            pantalla.blit(borde_superior, rect.move(-2, -2))

    def entrada_teclado(self):
        teclaPresionada = pygame.key.get_pressed()
        if teclaPresionada[K_UP]:
            return ARRIBA
        if teclaPresionada[K_DOWN]:
            return ABAJO
        if teclaPresionada[K_LEFT]:
            return IZQUIERDA
        if teclaPresionada[K_RIGHT]:
            return DERECHA
        return STOP

    def comer_pellets(self, lista_pellets):
        for pellet in lista_pellets:
            distancia = self.posicion - pellet.posicion
            if distancia.magnitudCuadrada() <= (self.radio + pellet.radioColision) ** 2:
                pellet.visible = False  # Oculta el pellet cuando es comido
                return pellet
        return None

    def actualizar_skin(self):
        """Cambia la skin de Pacman al siguiente fotograma, manteniendo la última dirección válida si se detiene."""
        # Mantén la última dirección animada si la dirección actual es STOP
        direccion_animacion = self.direccion if self.direccion != STOP else self.direccion_deseada

        # Verifica si la dirección de animación es válida
        if direccion_animacion not in self.skins:
            # Si no es válida, restablece a la última dirección válida
            direccion_animacion = DERECHA  # o cualquier otra dirección que desees como predeterminada

        # Cambiar al siguiente fotograma de la animación en la dirección seleccionada
        self.skin_index = (self.skin_index + 1) % len(self.skins[direccion_animacion])
        self.skin = self.skins[direccion_animacion][self.skin_index]
