from tkinter.constants import RIGHT
import pygame
from Entidad import Entidad
from Constantes import *
from random import choice


class Fruta(Entidad):
    """
    Clase que representa las frutas que aparecen durante el juego de Pac-Man.
    Hereda de la clase Entidad y maneja la lógica de aparición, visualización
    y desaparición de frutas con diferentes sprites.
    """
    # Variable de clase para evitar que se repita la misma fruta consecutivamente
    ultima_fruta = None

    def __init__(self, nodo):
        """
        Inicializa una nueva fruta.

        Args:
            nodo: Nodo del grafo donde aparecerá la fruta
        """
        Entidad.__init__(self, nodo)

        # Atributos de identificación
        self.nombre = FRUTA
        self.color = BLANCO

        # Atributos de tiempo y estado
        self.tiempo = 5  # Duración en pantalla en segundos
        self.temporizador = 0  # Contador de tiempo transcurrido
        self.desaparecer = False  # Indica si la fruta debe desaparecer
        self.puntos = 100  # Puntos que otorga al ser comida

        # Atributos de visualización
        self.tamano_fruta = (25, 25)  # Dimensiones uniformes para todas las frutas
        self.en_pantalla = False  # Estado de visualización

        # Inicialización de sprites
        self.cargar_imagenes()
        # Selecciona una fruta diferente a la última que apareció
        self.skin = self.seleccionar_fruta_diferente()

        # Configuración inicial de posición
        self.establecer_entre_nodos(DERECHA)

    def cargar_imagenes(self):
        """
        Carga y prepara los sprites de las frutas.
        Cada fruta tiene un comodín único y se redimensiona al tamaño estándar.
        """
        self.imagenes = []
        # Lista de comodines para los nombres de archivo
        comodines = ['fres', 'vai', 'choco', 'pach']

        # Intenta cargar cada imagen de fruta
        for comodin in comodines:
            try:
                # Carga la imagen original
                imagen_original = pygame.image.load(f"multimedia/comodin_{comodin}.png").convert_alpha()
                # Redimensiona la imagen al tamaño estándar
                imagen_redimensionada = pygame.transform.scale(imagen_original, self.tamano_fruta)
                # Almacena el tipo de fruta y su imagen
                self.imagenes.append((comodin, imagen_redimensionada))
            except pygame.error:
                print(f"No se pudo cargar la imagen de {comodin}")

        # Si no se pudo cargar ninguna imagen, crea una superficie por defecto
        if not self.imagenes:
            print("No se pudieron cargar las imágenes de frutas")
            superficie_default = pygame.Surface(self.tamano_fruta)
            superficie_default.fill(self.color)
            self.imagenes = [('default', superficie_default)]

    def seleccionar_fruta_diferente(self):
        """
        Selecciona aleatoriamente una fruta diferente a la última utilizada.

        Returns:
            Surface: Imagen de la fruta seleccionada
        """
        # Filtra las frutas disponibles excluyendo la última utilizada
        frutas_disponibles = [fruta for fruta in self.imagenes if fruta[0] != Fruta.ultima_fruta]

        # Si no hay frutas diferentes disponibles, usa todas
        if not frutas_disponibles:
            frutas_disponibles = self.imagenes

        # Selecciona una fruta aleatoria
        fruta_seleccionada = choice(frutas_disponibles)

        # Actualiza el registro de la última fruta
        Fruta.ultima_fruta = fruta_seleccionada[0]

        # Retorna la imagen de la fruta
        return fruta_seleccionada[1]

    def actualizar(self, dt):
        self.temporizador += dt
        if self.temporizador >= self.tiempo:
            self.desaparecer = True

    def render(self, pantalla):
        if self.visible and not self.desaparecer:
            if self.skin:
                # Obtiene la posición como tupla de enteros
                p = self.posicion.entero()
                # Centra la imagen en la posición actual
                rect = self.skin.get_rect(center=p)
                # Dibuja la imagen de la fruta
                pantalla.blit(self.skin, rect)
            else:
                # Dibuja un círculo como fallback si no hay imagen
                p = self.posicion.entero()
                pygame.draw.circle(pantalla, self.color, p, self.radio)