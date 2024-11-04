import pygame
from Pacman import *
from Constantes import *
from Vector import Vector1

class Texto(object):
    def __init__(self, texto, color, x, y, tamaño, tiempo=None, id=None, visible=True):
        # inicializa atributos de texto, color, posicion, tamaño y visibilidad
        self.id = id
        self.texto = texto
        self.color = color
        self.tamaño = tamaño
        self.visible = visible
        self.posicion = Vector1(x, y)
        self.temporizador = 0
        self.duracion = tiempo
        self.etiqueta = None
        self.destruir = False
        # configura una fuente por defecto
        self.configurarFuente("Fuentes/PressStart2P-Regular.ttf")
        self.crearEtiqueta()  # inicializa la etiqueta de texto a mostrar

    def configurarFuente(self, ruta_fuente):
        # intenta cargar una fuente personalizada desde la ruta indicada, usa Arial como respaldo si falla
        try:
            self.fuente = pygame.font.Font(ruta_fuente, self.tamaño)
        except:
            self.fuente = pygame.font.SysFont('Arial', self.tamaño)

    def crearEtiqueta(self):
        # renderiza el texto como una imagen en la etiqueta con el color indicado
        self.etiqueta = self.fuente.render(self.texto, 1, self.color)

    def setTexto(self, nuevo_texto):
        # actualiza el texto mostrado en la etiqueta
        self.texto = str(nuevo_texto)
        self.crearEtiqueta()

    def actualizar(self, dt):
        # controla el tiempo de duracion del texto en pantalla y lo elimina si se cumple el tiempo
        if self.duracion is not None:
            self.temporizador += dt
            if self.temporizador >= self.duracion:
                self.temporizador = 0
                self.duracion = None
                self.destruir = True

    def renderizar(self, pantalla):
        # muestra el texto en la pantalla si es visible
        if self.visible:
            x = self.posicion.x
            y = self.posicion.y
            pantalla.blit(self.etiqueta, (x, y))


class GrupoTexto(object):
    def __init__(self):
        # inicializa un grupo de textos y configura los textos iniciales
        self.proximo_id = 10
        self.todos_los_textos = {}
        self.configurarTextos()


    def agregarTexto(self, texto, color, x, y, tamaño, tiempo=None, id=None):
        # agrega un nuevo texto al grupo de textos y le asigna un id
        self.proximo_id += 1
        self.todos_los_textos[self.proximo_id] = Texto(texto, color, x, y, tamaño, tiempo=tiempo, id=id)
        return self.proximo_id

    def eliminarTexto(self, id):
        # elimina un texto del grupo usando su id
        self.todos_los_textos.pop(id)

    def configurarTextos(self):
        # configura los textos iniciales del juego como el puntaje, nivel, listo, pausa y fin del juego
        tamaño = ALTURACELDA
        self.todos_los_textos[SCORETXT] = Texto("0".zfill(8), BLANCO, 0, ALTURACELDA, tamaño)
        self.todos_los_textos[LEVELTXT] = Texto(str(1).zfill(3), BLANCO, 23 * ANCHOCELDA, ALTURACELDA, tamaño)
        self.todos_los_textos[READYTXT] = Texto("¡LISTO!", AMARILLO, 11.25 * ANCHOCELDA, 20 * ALTURACELDA, tamaño,
                                                visible=False)
        self.todos_los_textos[PAUSETXT] = Texto("¡PAUSA!", AMARILLO, 10.625 * ANCHOCELDA, 20 * ALTURACELDA, tamaño,
                                                visible=False)
        self.todos_los_textos[GAMEOVERTXT] = Texto("¡FIN DEL JUEGO!", AMARILLO, 10 * ANCHOCELDA, 20 * ALTURACELDA,
                                                   tamaño, visible=False)
        self.agregarTexto("PUNTOS", BLANCO, 0, 0, tamaño)
        self.agregarTexto("NIVEL", BLANCO, 23 * ANCHOCELDA, 0, tamaño)

    def actualizar(self, dt):
        # actualiza todos los textos del grupo y elimina los que se hayan destruido
        for tkey in list(self.todos_los_textos.keys()):
            # self.todos_los_textos[tkey].actualizar(dt)
            if self.todos_los_textos[tkey].destruir:
                self.eliminarTexto(tkey)

    def mostrarTexto(self, id):
        # muestra solo un texto específico, oculta los demás
        self.ocultarTexto()
        self.todos_los_textos[id].visible = True

    def ocultarTexto(self):
        # oculta textos específicos como listo, pausa y fin del juego
        self.todos_los_textos[READYTXT].visible = False
        self.todos_los_textos[PAUSETXT].visible = False
        self.todos_los_textos[GAMEOVERTXT].visible = False

    def actualizarPuntaje(self, puntaje):
        # actualiza el texto del puntaje a un nuevo valor
        self.actualizarTexto(SCORETXT, str(puntaje).zfill(8))

    def actualizarNivel(self, nivel):
        # actualiza el texto del nivel a un nuevo valor
        self.actualizarTexto(LEVELTXT, str(nivel + 1).zfill(3))

    def actualizarTexto(self, id, valor):
        # actualiza el texto de un id específico con un nuevo valor
        if id in self.todos_los_textos.keys():
            self.todos_los_textos[id].setTexto(valor)

    def renderizar(self, pantalla):
        # renderiza todos los textos en la pantalla
        for tkey in list(self.todos_los_textos.keys()):
            self.todos_los_textos[tkey].renderizar(pantalla)
