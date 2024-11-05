import pygame
from pygame.locals import *
from Vector import Vector1
from Constantes import *
from Entidad import Entidad


class Pacman(Entidad):
    def __init__(self, nodo):
        super().__init__(nodo)  # Llamada al constructor de la clase padre
        self.nombre = PACMAN
        self.color = AMARILLO
        self.velocidad = 100 * ANCHOCELDA / 16  # Sobreescribe la velocidad del padre
        # Atributos específicos de Pacman
        self.direccion_deseada = STOP
        self.tiene_poder = False
        self.tiempo_poder = 0
        self.duracion_poder = 7
        self.fantasmas = []
        # Inicialización de la animación
        self.cargar_animaciones()
        self.skin = self.skins[DERECHA][0]  # Imagen inicial

    def cargar_animaciones(self):
        # Diccionario para almacenar las animaciones por dirección
        self.skins = {
            ARRIBA: [],
            ABAJO: [],
            IZQUIERDA: [],
            DERECHA: []
        }

        # Cargar las imágenes para cada dirección
        for i in range(1, 7):  # Del 1 al 6 según los archivos que veo
            # Cargar arriba
            arr = pygame.image.load(f"multimedia/{i}_Arr.png").convert_alpha()
            self.skins[ARRIBA].append(arr)

            # Cargar abajo
            aba = pygame.image.load(f"multimedia/{i}_Aba.png").convert_alpha()
            self.skins[ABAJO].append(aba)

            # Cargar derecha
            der = pygame.image.load(f"multimedia/{i}_Der.png").convert_alpha()
            self.skins[DERECHA].append(der)

            # Cargar izquierda
            izq = pygame.image.load(f"multimedia/{i}_Izq.png").convert_alpha()
            self.skins[IZQUIERDA].append(izq)

    def activar_poder(self):
        """Activa el poder y cambia el modo de los fantasmas."""
        self.tiene_poder = True
        self.tiempo_poder = self.duracion_poder
        for fantasma in self.fantasmas:
            fantasma.set_scatter_mode()

    def actualizar_poder(self, dt):
        """Actualiza el estado del poder."""
        if self.tiene_poder:
            self.tiempo_poder -= dt
            if self.tiempo_poder <= 0:
                self.tiene_poder = False
                self.tiempo_poder = 0
                for fantasma in self.fantasmas:
                    fantasma.modo = CHASE

    def comer_pellets(self, lista_pellets):
        """Verifica colisiones con pellets."""
        for pellet in lista_pellets:
            distancia = self.posicion - pellet.posicion
            distancia_potencia = distancia.magnitudCuadrada()
            radio_potencia = (pellet.radio + self.radio_colision) ** 2

            if distancia_potencia <= radio_potencia:
                if pellet.nombre == PELLETPODER:
                    self.activar_poder()
                return pellet
        return None

    def actualizar(self, dt):
        """Actualiza el estado de Pacman."""
        self.actualizar_animacion(dt)
        self.actualizar_poder(dt)

        # Actualizar posición actual
        self.posicion += self.direcciones[self.direccion] * self.velocidad * dt

        direccion = self.entrada_teclado()
        if direccion != STOP:
            self.direccion_deseada = direccion

        if self.blanco_sobrepasado():
            self.nodo = self.blanco

            if self.nodo.vecinos[PORTAL] is not None:
                self.nodo = self.nodo.vecinos[PORTAL]

            if self.direccion_deseada != STOP:
                if self.validar_direccion(self.direccion_deseada):
                    self.direccion = self.direccion_deseada
                    self.direccion_deseada = STOP

            self.blanco = self.get_nuevo_blanco(self.direccion)

            if self.blanco is self.nodo:
                self.direccion = STOP

            self.set_posicion()
        else:
            if self.direccion_opuesta(direccion):
                self.direccion_reversa()

    def render(self, pantalla):
        """Renderiza a Pacman en la pantalla"""
        if self.visible:
            if self.skin:
                # Obtener la posición como tupla de enteros
                p = self.posicion.entero()

                # Obtener el rectángulo de la imagen centrado en la posición actual
                rect = self.skin.get_rect(center=p)


                # Dibujar la imagen actual de la animación
                pantalla.blit(self.skin, rect)


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