from tkinter.constants import RIGHT
import pygame
from Entidad import Entidad
from Constantes import *
from random import choice


class Fruta(Entidad):
    # Variable de clase para rastrear la última fruta utilizada
    ultima_fruta = None

    def __init__(self, nodo):
        Entidad.__init__(self, nodo)
        self.nombre = FRUTA
        self.color = BLANCO
        self.tiempo = 5
        self.temporizador = 0
        self.desaparecer = False
        self.puntos = 100
        self.tamano_fruta = (25, 25)# Tamaño deseado para todas las frutas
        self.en_pantalla = False


        # Cargar la imagen de la fruta
        self.cargar_imagenes()
        self.skin = self.seleccionar_fruta_diferente()  # Usar una fruta diferente a la última

        self.establecer_entre_nodos(DERECHA)

    def cargar_imagenes(self):
        """Carga las imágenes de la fruta y las redimensiona"""
        self.imagenes = []
        comodines = ['fres', 'vai', 'choco','pach']

        for comodin in comodines:
            try:
                imagen_original = pygame.image.load(f"multimedia/comodin_{comodin}.png").convert_alpha()
                # Redimensionar la imagen al tamaño especificado
                imagen_redimensionada = pygame.transform.scale(imagen_original, self.tamano_fruta)
                self.imagenes.append((comodin, imagen_redimensionada))  # Guardamos el tipo y la imagen
            except pygame.error:
                print(f"No se pudo cargar la imagen de {comodin}")

        if not self.imagenes:
            print("No se pudieron cargar las imágenes de frutas")
            # Crear una superficie por defecto si no hay imágenes
            superficie_default = pygame.Surface(self.tamano_fruta)
            superficie_default.fill(self.color)
            self.imagenes = [('default', superficie_default)]

    def seleccionar_fruta_diferente(self):
        """Selecciona una fruta diferente a la última utilizada"""
        frutas_disponibles = [fruta for fruta in self.imagenes if fruta[0] != Fruta.ultima_fruta]

        if not frutas_disponibles:
            # Si no hay frutas disponibles diferentes, usar todas
            frutas_disponibles = self.imagenes

        # Seleccionar una fruta aleatoria de las disponibles
        fruta_seleccionada = choice(frutas_disponibles)

        # Actualizar la última fruta utilizada
        Fruta.ultima_fruta = fruta_seleccionada[0]

        # Devolver la imagen de la fruta
        return fruta_seleccionada[1]

    def actualizar(self, dt):
        self.temporizador += dt
        if self.temporizador >= self.tiempo:
            self.desaparecer = True

    def render(self, pantalla):
        """Dibuja la fruta en la pantalla usando su imagen"""
        if self.visible and not self.desaparecer:
            if self.skin:
                # Obtener la posición como tupla de enteros
                p = self.posicion.entero()
                # Obtener el rectángulo de la imagen centrado en la posición actual
                rect = self.skin.get_rect(center=p)
                # Dibujar la imagen
                pantalla.blit(self.skin, rect)
            else:
                # Fallback al círculo si no hay imagen
                p = self.posicion.entero()
                pygame.draw.circle(pantalla, self.color, p, self.radio)