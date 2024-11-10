import pygame
from random import random
from Entidad import Entidad
from Constantes import *


class Fruta(Entidad):
    """
    Clase que representa las frutas que aparecen durante el juego de Pac-Man.
    Hereda de la clase Entidad y maneja la lógica de aparición, visualización
    y desaparición de frutas con diferentes sprites.
    """

    def __init__(self, nodo, nivel,grupo_texto):
        """
        Inicializa una nueva fruta.
        """
        Entidad.__init__(self, nodo)

        Entidad.__init__(self, nodo)

        # Atributos básicos
        self.nombre = FRUTA
        self.color = BLANCO
        self.visible = True
        self.tiempo = 5
        self.temporizador = 0
        self.desaparecer = False
        self.grupo_texto = grupo_texto  # Guardamos la referencia a grupo_texto
        self.nivel = nivel  # Guardamos el nivel para saber qué fruta es

        # Mapeo de frutas por nivel
        self.frutas_por_nivel = {
            1: ('fres', 100),  # (nombre_archivo, puntos)
            2: ('vai', 200),
            3: ('choco', 300)
        }

        # Atributos de visualización
        self.tamano_fruta = (30, 30)
        self.cargar_imagenes()

        # 20% de probabilidad de que aparezca la pacha
        if random() < 0.2:
            self.skin = self.pacha
            self.puntos = 500
            self.tipo_fruta = 'pach'
        else:
            self.skin = self.seleccionar_fruta_por_nivel(nivel)
            self.puntos = self.frutas_por_nivel.get(nivel, (None, 100))[1]
            self.tipo_fruta = self.frutas_por_nivel.get(nivel, ('fres', 100))[0]  # Por defecto 'fres'

        # Configuración de posición
        self.establecer_entre_nodos(DERECHA)

    def cargar_imagenes(self):
        """
        Carga y prepara los imagenes para cada frutas.
        """
        self.imagenes = {}  # Usamos un diccionario para mapear nivel->imagen

        # Cargar frutas normales
        for nivel, (comodin, _) in self.frutas_por_nivel.items():
            ruta = f"multimedia/comodin_{comodin}.png"
            try:
                imagen = pygame.image.load(ruta)
                imagen = pygame.transform.scale(imagen, self.tamano_fruta)
                self.imagenes[nivel] = imagen
                print(f"Fruta nivel {nivel} cargada: {comodin}")
            except pygame.error as e:
                print(f"Error al cargar la imagen {ruta}: {e}")
                # Crear una superficie de fallback para este nivel
                superficie = pygame.Surface(self.tamano_fruta)
                superficie.fill((255, 0, 0))
                self.imagenes[nivel] = superficie

        # Cargar la pacha
        try:
            ruta_pacha = "multimedia/comodin_pach.png"
            self.pacha = pygame.image.load(ruta_pacha)
            self.pacha = pygame.transform.scale(self.pacha, self.tamano_fruta)
            print("Pacha cargada exitosamente")
        except pygame.error as e:
            print(f"Error al cargar la pacha: {e}")
            superficie = pygame.Surface(self.tamano_fruta)
            superficie.fill((0, 255, 0))  # Verde para distinguir el error de pacha
            self.pacha = superficie

    def seleccionar_fruta_por_nivel(self, nivel):
        """
        Selecciona la fruta específica para el nivel actual.
        """
        return self.imagenes.get(nivel, self.imagenes.get(1))  # Fallback al nivel 1 si el nivel no existe

    def actualizar(self, dt):
        """
        Actualiza el estado de la fruta.
        """
        self.temporizador += dt
        if self.temporizador >= self.tiempo:
            self.desaparecer = True

    def render(self, pantalla):
        """
        Renderiza la fruta en pantalla.
        """
        if self.visible and not self.desaparecer:
            if self.skin:
                p = self.posicion.entero()
                rect = self.skin.get_rect(center=p)
                pantalla.blit(self.skin, rect)
            else:
                p = self.posicion.entero()
                pygame.draw.circle(pantalla, (255, 0, 0), p, 15)

    def ser_comido(self):
        self.grupo_texto.agregarFruta(self.tipo_fruta)
        self.desaparecer = True


