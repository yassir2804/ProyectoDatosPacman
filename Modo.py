from Constantes import *
from Entidad import *

class Controladora_Modos(object):
    """
        Clase encargada de controlar los diferentes modos de comportamiento de los fantasmas
        en el juego Pac-Man. Maneja los modos SCATTER, CHASE, FREIGHT y SPAWN. A traves de
        esta clase se actualiza el estado de los fantasmas, cambiando entre los modos según
        el tiempo y las condiciones del juego. Esta clase interactua con la clase `ModoPrincipal`
        para manejar las transiciones de los modos y también con las entidades, como los fantasmas,
        para ejecutar las acciones correspondientes en cada modo.
    """

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
        elif self.current in [SCATTER, CHASE]:
            self.current = self.modoPrincipal.modo
        elif self.current is not SPAWN:  # No actualizar si está en modo SPAWN
            self.current = self.modoPrincipal.modo

    def modo_freight(self):
        if self.current in [SCATTER, CHASE]:
            self.temporizador = 0
            self.tiempo = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.temporizador = 0

    def modo_chase(self):
        if self.current in [FREIGHT]:
            self.temporizador = 0
            self.tiempo = 20
            self.current = SCATTER
        elif self.current is SCATTER:
            self.temporizador = 0

    def set_modo_spawn(self):
        self.current = SPAWN
        self.temporizador = 0
        self.tiempo = None

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
