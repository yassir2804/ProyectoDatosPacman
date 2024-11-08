import pygame
from Constantes import *


class LevelManager:
    def __init__(self):
        self.nivel_actual = 1
        self.velocidad_base_fantasmas = 100  # Velocidad inicial de los fantasmas
        self.factor_velocidad = 1.2  # Factor de incremento de velocidad por nivel

    def subir_nivel(self):
        if self.nivel_actual >= 3:
            return False

        self.nivel_actual += 1
        return True

    def obtener_velocidad_fantasmas(self):
        return self.velocidad_base_fantasmas * (self.factor_velocidad ** (self.nivel_actual - 1))

    def verificar_nivel_completado(self, Pellet):

        return len(Pellet.listaPellets) == 0