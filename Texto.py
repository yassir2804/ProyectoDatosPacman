import pygame
from Constantes import *
from Vector import Vector1


class Texto(object):
    """
           Clase que representa a Pacman, el personaje principal del juego. Esta clase gestiona
           el comportamiento de Pacman en el juego, incluyendo el movimiento, las colisiones con
           pellets y fantasmas, el manejo de vidas, la activacion de poderes, las animaciones y
           los sonidos. Pacman puede morir, resucitar, comer pellets, y activar el modo de poder
           para comer fantasmas. Tambien gestiona la interacción con los nodos y las animaciones
           correspondientes en cada dirección.
           """

    def __init__(self, texto, color, x, y, tamaño, tiempo=None, id=None, visible=True):
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
        self.configurarFuente("Fuentes/PressStart2P-Regular.ttf")
        self.crearEtiqueta()

    def configurarFuente(self, ruta_fuente):
        try:
            self.fuente = pygame.font.Font(ruta_fuente, self.tamaño)
        except:
            self.fuente = pygame.font.SysFont('Arial', self.tamaño)

    def crearEtiqueta(self):
        self.etiqueta = self.fuente.render(self.texto, 1, self.color)

    def setTexto(self, nuevo_texto):
        self.texto = str(nuevo_texto)
        self.crearEtiqueta()

    def renderizar(self, pantalla):
        if self.visible:
            x = self.posicion.x
            y = self.posicion.y
            pantalla.blit(self.etiqueta, (x, y))


class GrupoTexto(object):
    def __init__(self):
        self.proximo_id = 10
        self.todos_los_textos = {}
        self.configurarTextos()
        self.vidas = 3  # Número inicial de vidas
        self.cargar_imagen_vida()
        self.cargar_imagen_frutas()
        self.frutas_comidas = [] # Inicializa el contador de frutas
        self.game_over_visible = False
        self.nombres_frutas = ["Cereza", "Naranja", "Manzana"]  # Nombres de las frutas para referencia

    def cargar_imagen_vida(self):
        self.imagen_vida = pygame.image.load("multimedia/Vidas.png").convert_alpha()
        self.imagen_vida = pygame.transform.scale(self.imagen_vida, (45, 45))

    def cargar_imagen_frutas(self):
        # Lista de rutas de las imágenes de frutas
        rutas_frutas = [
            "multimedia/comodin_fres.png",
            "multimedia/comodin_vai.png",
            "multimedia/comodin_choco.png",
            "multimedia/comodin_pach.png"
        ]

        # Cargar y escalar todas las imágenes
        self.imagenes_frutas = []
        for ruta in rutas_frutas:
            try:
                imagen = pygame.image.load(ruta).convert_alpha()
                imagen_escalada = pygame.transform.scale(imagen, (45, 45))
                self.imagenes_frutas.append(imagen_escalada)
            except pygame.error as e:
                print(f"Error al cargar la imagen {ruta}: {e}")
                # Crear una imagen de respaldo en caso de error
                imagen_respaldo = pygame.Surface((45, 45))
                imagen_respaldo.fill(AMARILLO)
                self.imagenes_frutas.append(imagen_respaldo)

    def agregarTexto(self, texto, color, x, y, tamaño, tiempo=None, id=None):
        self.proximo_id += 1
        self.todos_los_textos[self.proximo_id] = Texto(texto, color, x, y, tamaño, tiempo=tiempo, id=id)
        return self.proximo_id

    def agregarFruta(self, tipo_fruta):
        self.frutas_comidas+=1
        if len(self.frutas_comidas) < 4:
            self.frutas_comidas.append(tipo_fruta)

    def configurarTextos(self):
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
        for tkey in list(self.todos_los_textos.keys()):
            if self.todos_los_textos[tkey].destruir:
                self.todos_los_textos.pop(tkey)

    def actualizarPuntaje(self, puntaje):
        if SCORETXT in self.todos_los_textos:
            self.todos_los_textos[SCORETXT].setTexto(str(puntaje).zfill(8))

    def actualizarVidas(self, vidas):
        self.vidas = vidas

    def obtenerNombreFruta(self, indice):
        """Retorna el nombre de la fruta según el índice"""
        return self.nombres_frutas[indice % len(self.nombres_frutas)]

    def renderizar(self, pantalla):
        # Renderizar todos los textos
        for tkey in list(self.todos_los_textos.keys()):
            self.todos_los_textos[tkey].renderizar(pantalla)

        # Renderizar las vidas (corazones)
        margen = 10
        separacion = 5
        for i in range(self.vidas):
            x = margen + i * (self.imagen_vida.get_width() + separacion)
            y = TAMANIOPANTALLA[1] - self.imagen_vida.get_height() - margen
            pantalla.blit(self.imagen_vida, (x, y))

        # Renderizar solo las frutas que han sido comidas
        for i, tipo_fruta in enumerate(self.frutas_comidas):
            x = TAMANIOPANTALLA[0] - (margen + (i + 1) * (45 + separacion))
            y = TAMANIOPANTALLA[1] - 45 - margen

            # Determinar qué imagen usar basado en el tipo de fruta
            if tipo_fruta == 'fres':
                indice_fruta = 0
            elif tipo_fruta == 'vai':
                indice_fruta = 1
            elif tipo_fruta == 'choco':
                indice_fruta = 2
            elif tipo_fruta == 'pach':
                indice_fruta = 3

            if 0 <= indice_fruta < len(self.imagenes_frutas):
                pantalla.blit(self.imagenes_frutas[indice_fruta], (x, y))
    def mostrar_game_over(self):
        self.game_over_visible = True

    def reset(self):
        """Reinicia el estado de las frutas y otros elementos"""
        self.frutas_comidas = []  # Vaciar la lista de frutas comidas
        self.game_over_visible = False