from Constantes import *
from Entidad import *


class ModoPrincipal(object):
    """
    Clase que maneja los modos principales de comportamiento de los fantasmas:
    SCATTER (dispersión) y CHASE (persecución).
    Alterna automáticamente entre estos dos modos según temporizadores.
    """

    def __init__(self):
        self.temporizador = 0  # Contador de tiempo actual
        self.scatter()  # Comienza en modo dispersión

    def actualizar(self, dt):
        """
        Actualiza el temporizador y cambia entre modos cuando corresponda.
        """
        self.temporizador += dt
        if self.temporizador >= self.tiempo:
            # Cambia al modo opuesto cuando se acaba el tiempo
            if self.modo is SCATTER:
                self.chase()  # Cambia a modo persecución
            elif self.modo is CHASE:
                self.scatter()  # Cambia a modo dispersión

    def scatter(self):
        """
        Establece el modo SCATTER (dispersión).
        Los fantasmas se dirigen a sus esquinas designadas.
        Duración: 7 segundos
        """
        self.modo = SCATTER
        self.tiempo = 7
        self.temporizador = 0

    def chase(self):
        """
        Establece el modo CHASE (persecución).
        Los fantasmas persiguen a Pacman según sus estrategias individuales.
        Duración: 20 segundos
        """
        self.modo = CHASE
        self.tiempo = 20
        self.temporizador = 0


class Controladora_Modos(object):
    """
    Controlador principal de todos los modos de los fantasmas.
    Maneja las transiciones entre los diferentes estados: SCATTER, CHASE, FREIGHT y SPAWN.
    """

    def __init__(self, entidad):
        self.temporizador = 0  # Contador de tiempo
        self.tiempo = None  # Duración del modo actual
        self.modoPrincipal = ModoPrincipal()  # Controlador de modos básicos
        self.current = self.modoPrincipal.modo  # Modo actual
        self.entidad = entidad  # Referencia al fantasma

    def actualizar(self, dt):
        self.modoPrincipal.actualizar(dt)

        if self.current is FREIGHT:
            # Manejo del modo FREIGHT (cuando los fantasmas son vulnerables)
            self.temporizador += dt
            if self.temporizador >= self.tiempo:
                self.temporizador += dt
                self.tiempo = None
                self.entidad.modo_normal()  # Vuelve al modo normal
                self.current = self.modoPrincipal.modo
        elif self.current in [SCATTER, CHASE]:
            # Actualización de modos normales
            self.current = self.modoPrincipal.modo
        elif self.current is not SPAWN:
            # Actualiza si no está en modo SPAWN (fantasma regresando a casa)
            self.current = self.modoPrincipal.modo

    def modo_freight(self):
        """
        Activa el modo FREIGHT (vulnerable) cuando Pacman come una power pill.
        Duración: 7 segundos
        """
        if self.current in [SCATTER, CHASE]:
            self.temporizador = 0
            self.tiempo = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            # Reinicia el temporizador si ya estaba en modo FREIGHT
            self.temporizador = 0

    def modo_chase(self):
        """
        Cambia al modo CHASE desde FREIGHT o reinicia el temporizador si ya está en SCATTER
        """
        if self.current in [FREIGHT]:
            self.temporizador = 0
            self.tiempo = 20
            self.current = SCATTER
        elif self.current is SCATTER:
            self.temporizador = 0

    def set_modo_spawn(self):
        """
        Establece el modo SPAWN cuando el fantasma es comido por Pacman.
        En este modo, el fantasma regresa a su casa para revivir.
        """
        self.current = SPAWN
        self.temporizador = 0
        self.tiempo = None  # El tiempo no es necesario en modo SPAWN, dura hasta llegar a casa