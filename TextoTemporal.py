import pygame

class TextoTemporal:
    def __init__(self, texto, posicion, duracion, fuente, color=(255, 255, 255)):
        self.texto = texto
        self.posicion = posicion
        self.duracion = duracion
        self.fuente = fuente
        self.color = color
        self.tiempo_creacion = pygame.time.get_ticks()

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_creacion > self.duracion:
            return False
        return True

    def render(self, pantalla):
        texto_surf = self.fuente.render(self.texto, True, self.color)
        pantalla.blit(texto_surf, self.posicion)
