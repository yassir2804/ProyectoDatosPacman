from Constantes import *
from Entidad import *
class Modo(object):
    def __init__(self):
        self.temporizador = 0
        self.tiempo = 20  # tiempo inicial
        self.modo = CHASE  # modo inicial

    def actualizar(self, dt):
        self.temporizador += dt
        if self.temporizador > self.tiempo:
            if self.modo is SCATTER:
                self.chase()
            elif self.modo is CHASE:
                self.scatter()
            else: 
                self.freight()

    def scatter(self):
        self.modo = SCATTER
        self.tiempo = 7 
        self.temporizador = 0

    def chase(self):
        self.modo = CHASE
        self.tiempo = 20
        self.temporizador = 0
        
    def freight(self):
        self.modo = FREIGHT
        self.tiempo = 7
        self.temporizador = 0

    def set_modo(self, nuevo_modo, tiempo=None):
        """Método para cambiar el modo externamente"""
        if nuevo_modo == SCATTER:
            self.modo = SCATTER
            self.tiempo = tiempo if tiempo is not None else 7
        elif nuevo_modo == CHASE:
            self.modo = CHASE
            self.tiempo = tiempo if tiempo is not None else 20
        else:
            self.modo = FREIGHT
            self.tiempo = tiempo if tiempo is not None else 7
        self.temporizador = 0


class Controladora_Modos(object):
    def __init__(self, entidad):
        self.modo = Modo()
        self.current = self.modo.modo
        self.entidad = entidad

    def actualizar(self, dt):
        self.modo.actualizar(dt)
        self.current = self.modo.modo

    def set_modo(self, nuevo_modo, tiempo=None):
        """Método para cambiar el modo desde fuera"""
        self.modo.set_modo(nuevo_modo, tiempo)
        self.current = self.modo.modo