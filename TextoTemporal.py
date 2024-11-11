import pygame

class TextoTemporal:
    def __init__(self, texto, posicion, duracion, fuente, color=(255, 255, 255)):
        """
        Constructor de la clase TextoTemporal
        Inicializa un texto que se mostrará temporalmente en la pantalla
        """
        # Texto a mostrar
        self.texto = texto
        # Tupla (x,y) donde se mostrará el texto
        self.posicion = posicion
        # Tiempo en milisegundos que el texto permanecerá visible
        self.duracion = duracion
        # Objeto Font de pygame para renderizar el texto
        self.fuente = fuente
        # Color del texto en formato RGB, por defecto blanco
        self.color = color
        # Guarda el momento de creación del texto
        self.tiempo_creacion = pygame.time.get_ticks()

    def actualizar(self):
        """
        Verifica si el texto debe seguir siendo mostrado
        Retorna False si el texto debe desaparecer, True si debe seguir visible
        """
        # Obtiene el tiempo actual
        tiempo_actual = pygame.time.get_ticks()
        # Si ha pasado más tiempo que la duración especificada
        if tiempo_actual - self.tiempo_creacion > self.duracion:
            return False  # El texto debe desaparecer
        return True  # El texto debe seguir mostrándose

    def render(self, pantalla):
        """
        Dibuja el texto en la pantalla
        """
        # Crea la superficie del texto con anti-aliasing (True) y el color especificado
        texto_surf = self.fuente.render(self.texto, True, self.color)
        # Dibuja el texto en la pantalla en la posición especificada
        pantalla.blit(texto_surf, self.posicion)
