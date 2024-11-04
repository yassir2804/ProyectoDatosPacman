from Constantes import *
from Entidad import *
class ModoPrincipal(object):
    def __init__(self):
        self.temporizador = 0
        self.scatter()

    def actualizar(self, dt):
        self.temporizador += dt
        if self.temporizador >= self.tiempo:
            if self.modo is SCATTER:
                self.chase()
            elif self.modo is CHASE:
                self.scatter()


    def scatter(self):
        self.modo = SCATTER
        self.tiempo = 7 
        self.temporizador = 0

    def chase(self):
        self.modo = CHASE
        self.tiempo = 20
        self.temporizador = 0


class Controladora_Modos(object):
    def __init__(self, entidad):
        self.temporizador = 0
        self.tiempo = None
        self.modoPrincipal = ModoPrincipal()
        self.current = self.modoPrincipal.modo
        self.entidad = entidad

    def actualizar(self, dt):
        self.modoPrincipal.actualizar(dt)
        if self.current is FREIGHT:
            self.temporizador += dt
            if self.temporizador >= self.tiempo:
                self.temporizador += dt
                self.tiempo = None
                self.entidad.modo_normal()
                self.current = self.modoPrincipal.modo
        else:
            self.current = self.modoPrincipal.modo

    def modo_freight(self):
        if self.current in [SCATTER, CHASE]:
            self.temporizador = 0
            self.tiempo = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.temporizador = 0