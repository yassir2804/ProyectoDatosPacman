import json
import pygame
from pygame import Vector2
from pygame.locals import *
from Constantes import *
from Fantasmas import GrupoFantasmas
from Grafo import Grafo
from Pacman import Pacman
from Pellet import GrupoPellets, Pellet, PelletPoder
from Texto import GrupoTexto

from Fruta import Fruta



class Controladora(object):
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMANIOPANTALLA, 0, 32)
        self.fondo = None
        self.clock = pygame.time.Clock()
        self.grafo = Grafo("mazetest.txt")
        self.grafo.set_portales((0, 17), (27, 17))

        self.game_over = False
        self.pausa = False

        # Crear Pacman primero
        self.pacman = Pacman(self.grafo.punto_partida_pacman())

        # Crear grupo de fantasmas
        self.fantasmas = GrupoFantasmas(nodo=self.grafo.obtener_nodo_desde_tiles(13, 16), pacman=self.pacman)
        self.fantasmas.blinky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(13, 16))
        self.fantasmas.clyde.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(18, 16))
        self.fantasmas.inky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(17, 20))
        self.fantasmas.pinky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(18, 16))

        # Inicializar temporizadores para la salida de fantasmas
        self.tiempo_transcurrido = 0
        self.tiempo_entre_fantasmas = 5  # segundos entre cada fantasma
        self.fantasmas_liberados = 0
        # Lista de fantasmas en orden de salida
        self.orden_fantasmas = [
            self.fantasmas.blinky,
            self.fantasmas.pinky,
            self.fantasmas.inky,
            self.fantasmas.clyde
        ]
        # Desactivar movimiento inicial de fantasmas
        for fantasma in self.orden_fantasmas[1:]:  # Todos excepto Blinky
            fantasma.activo = False
            fantasma.en_casa = True  # Nuevo estado para controlar si está en casa

        # Grupo de pellets y texto
        self.Pellet = GrupoPellets("mazetest.txt")
        self.grupo_texto = GrupoTexto()
        self.puntaje = 0
        self.tiempo_poder = 0
        self.duracion_poder = 7

        #Frutas
        self.fruta = None


    def verificacion_pellets(self):
        """
        Verifica la colisión con pellets y actualiza el puntaje.
        También maneja la activación del modo freight y los puntos por comer fantasmas.
        """
        # Verificar colisión con pellets
        pellet = self.pacman.comer_pellets(self.Pellet.listaPellets)
        if pellet:
            self.Pellet.numComidos += 1
            if pellet.nombre == PELLETPODER:
                self.puntaje += 50  # Más puntos por power pellet
                self.fantasmas.modo_Freight()  # Esto ya establece los puntos base en 200
                self.tiempo_poder = self.duracion_poder
            else:
                self.puntaje += 10  # Puntos normales por pellet regular
            self.grupo_texto.actualizarPuntaje(self.puntaje)
            self.Pellet.listaPellets.remove(pellet)

        # Verificar colisión con fantasmas
        puntos_fantasma = self.pacman.colision_con_fantasmas(self.fantasmas)
        if puntos_fantasma > 0:
            self.puntaje += puntos_fantasma
            self.grupo_texto.actualizarPuntaje(self.puntaje)

    def verificar_vidas(self):
        """Verifica el estado de las vidas y maneja el game over"""
        # Verificar colisiones con fantasmas
        puntos = self.pacman.colision_con_fantasmas(self.fantasmas)
        if puntos > 0:
            self.puntaje += puntos
            self.grupo_texto.actualizarPuntaje(self.puntaje)

        # Actualizar display de vidas cuando cambian
        self.grupo_texto.actualizarVidas(self.pacman.vidas)

        # Verificar game over
        if self.pacman.vidas <= 0 and not self.game_over:
            self.game_over = True
            self.fantasmas.esconder()  # Ocultar fantasmas
            self.grupo_texto.mostrar_game_over()

    def reset_nivel(self):
        """Resetea las posiciones de todos los personajes"""
        self.pacman.reset_posicion()
        self.fantasmas.reset()
        self.fantasmas.mostrar()
        # Resetear temporizadores de fantasmas
        self.tiempo_transcurrido = 0
        self.fantasmas_liberados = 0
        # Desactivar todos los fantasmas excepto Blinky
        for fantasma in self.orden_fantasmas[1:]:
            fantasma.activo = False
            fantasma.en_casa = True  # Resetear estado de casa

    def actualizar_temporizador_fantasmas(self, dt):
        """Maneja la liberación temporizada de los fantasmas"""
        if self.fantasmas_liberados < len(self.orden_fantasmas):
            self.tiempo_transcurrido += dt

            # Calcular cuántos fantasmas deberían estar activos
            fantasmas_a_liberar = int(self.tiempo_transcurrido // self.tiempo_entre_fantasmas)

            # Activar los fantasmas que correspondan
            while self.fantasmas_liberados < fantasmas_a_liberar and \
                    self.fantasmas_liberados < len(self.orden_fantasmas):
                fantasma = self.orden_fantasmas[self.fantasmas_liberados]
                fantasma.liberar_de_casa()  # Nuevo método para liberar fantasma
                self.fantasmas_liberados += 1

    def actualizar(self):
        if not self.game_over and not self.pausa:  # Añadir verificación de pausa
            dt = self.clock.tick(30) / 1000.0

            if not self.pacman.muerto:
                self.actualizar_temporizador_fantasmas(dt)
                self.pacman.actualizar(dt)
                self.fantasmas.actualizar(dt)
                self.Pellet.actualizar(dt)
                if self.fruta is not None:
                    self.fruta.actualizar(dt)

                self.verificacion_pellets()
            else:
                self.pacman.actualizar(dt)
                if not self.pacman.muerto:
                    self.reset_nivel()

            self.grupo_texto.actualizar(dt)
            self.verificar_vidas()
            self.verificar_eventos()
            self.verificar_fruta()
            self.render()
        else:
            self.verificar_eventos()
            self.render()

    def setFondo(self):
        self.fondo = pygame.surface.Surface(TAMANIOPANTALLA).convert()
        self.fondo.fill(NEGRO)

    def empezar(self):
        self.setFondo()

    def verificar_eventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if not self.pausa:
                        self.crear_menu_pausa()
                    else:
                        self.pausa = False
                elif self.pausa:
                    if event.key == K_UP:
                        self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones_pausa)
                    elif event.key == K_DOWN:
                        self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones_pausa)
                    elif event.key == K_RETURN:
                        self.ejecutar_opcion_pausa()

    def render(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.grafo.render(self.pantalla)
        self.Pellet.render(self.pantalla)
        self.pacman.render(self.pantalla)
        self.fantasmas.render(self.pantalla)
        if self.fruta is not None:
            self.fruta.render(self.pantalla)
        self.grupo_texto.renderizar(self.pantalla)
        if self.pausa:
            self.dibujar_menu_pausa()
        pygame.display.update()

    def verificar_fruta(self):
        """Verifica eventos relacionados con la fruta"""
        # Crear fruta cuando se hayan comido cierta cantidad de pellets
        if self.Pellet.numComidos == 50 or self.Pellet.numComidos == 140:
            if self.fruta is None:
                self.fruta = Fruta(self.grafo.obtener_nodo_desde_tiles(13, 20))

        # Verificar colisiones o si la fruta debe desaparecer
        if self.fruta is not None:
            if self.pacman.colision_fruta(self.fruta):
                self.puntaje += self.fruta.puntos  # Aumentar puntaje al comer la fruta
                self.grupo_texto.actualizarPuntaje(self.puntaje)
                self.fruta = None
            elif self.fruta.desaparecer:
                self.fruta = None

    def guardar_estado(self, archivo):
        estado = {
            'pacman': {
                'posicion': [self.pacman.posicion.x, self.pacman.posicion.y],
                'vidas': self.pacman.vidas,
                'puntos': self.puntaje
            },
            'fantasmas': [
                {
                    'nombre': fantasma.nombre,
                    'posicion': [fantasma.posicion.x, fantasma.posicion.y],
                    'modo': fantasma.modo.current
                } for fantasma in self.orden_fantasmas
            ],
            'fruta': {
                'posicion': [self.fruta.posicion.x, self.fruta.posicion.y] if self.fruta else None,
                'puntos': self.fruta.puntos if self.fruta else None
            },
            'pellets': [
                {
                    'fila': pellet.posicion.y // ALTURACELDA,
                    'columna': pellet.posicion.x // ANCHOCELDA,
                    'tipo': pellet.nombre
                } for pellet in self.Pellet.listaPellets
            ],
            'tiempo_poder': self.tiempo_poder
        }
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                contenido = json.dumps(estado, indent=4, ensure_ascii=False)
                f.write(contenido)
            return True
        except Exception as e:
            print(f"Error al guardar el estado: {str(e)}")
            return False

    def cargar_estado(self, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                estado = json.load(f)

            # Restaurar Pacman
            self.pacman.posicion = Vector2(estado['pacman']['posicion'][0],
                                           estado['pacman']['posicion'][1])
            self.pacman.vidas = estado['pacman']['vidas']
            self.puntaje = estado['pacman']['puntos']

            # Restaurar fantasmas
            for fantasma, datos in zip(self.orden_fantasmas, estado['fantasmas']):
                fantasma.posicion = Vector2(datos['posicion'][0], datos['posicion'][1])
                fantasma.modo.current = datos['modo']

            # Restaurar fruta
            if estado['fruta']['posicion']:
                pos = estado['fruta']['posicion']
                self.fruta = Fruta(Vector2(pos[0], pos[1]))
                self.fruta.puntos = estado['fruta']['puntos']
            else:
                self.fruta = None

            # Restaurar pellets
            self.Pellet.listaPellets.clear()
            self.Pellet.pelletsPoder.clear()
            for pellet_data in estado['pellets']:
                fila = pellet_data['fila']
                columna = pellet_data['columna']
                if pellet_data['tipo'] == PELLET:
                    nuevo_pellet = Pellet(fila, columna)
                    self.Pellet.listaPellets.append(nuevo_pellet)
                elif pellet_data['tipo'] == PELLETPODER:
                    nuevo_pellet = PelletPoder(fila, columna)
                    self.Pellet.listaPellets.append(nuevo_pellet)
                    self.Pellet.pelletsPoder.append(nuevo_pellet)

            self.tiempo_poder = estado['tiempo_poder']

            # Actualizar UI
            if hasattr(self, 'grupo_texto'):
                self.grupo_texto.actualizarPuntaje(self.puntaje)
                self.grupo_texto.actualizarVidas(self.pacman.vidas)

            return True

        except Exception as e:
            print(f"Error al cargar el estado: {str(e)}")
            return False

    def crear_menu_pausa(self):
        self.pausa = True
        self.opciones_pausa = ["Reanudar", "Guardar Partida", "Salir"]
        self.opcion_seleccionada = 0

        # Configuración del menú
        ANCHO_MENU = 300
        ALTO_MENU = 200
        self.superficie_pausa = pygame.Surface((ANCHO_MENU, ALTO_MENU))
        self.superficie_pausa.fill(NEGRO)  # Usar tu constante NEGRO
        self.rect_pausa = self.superficie_pausa.get_rect()
        self.rect_pausa.center = (TAMANIOPANTALLA[0] // 2, TAMANIOPANTALLA[1] // 2)

    def dibujar_menu_pausa(self):
        if not self.pausa:
            return

        # Oscurecer el fondo
        s = pygame.Surface(TAMANIOPANTALLA)
        s.set_alpha(128)
        s.fill(NEGRO)
        self.pantalla.blit(s, (0, 0))

        # Dibujar el menú
        pygame.draw.rect(self.superficie_pausa, NEGRO, self.superficie_pausa.get_rect())
        pygame.draw.rect(self.superficie_pausa, (255, 255, 255), self.superficie_pausa.get_rect(), 2)

        # Dibujar opciones
        font = pygame.font.Font(None, 36)
        for i, opcion in enumerate(self.opciones_pausa):
            color = (255, 255, 0) if i == self.opcion_seleccionada else (255, 255, 255)
            texto = font.render(opcion, True, color)
            rect_texto = texto.get_rect()
            rect_texto.centerx = self.superficie_pausa.get_width() // 2
            rect_texto.y = 50 + i * 50
            self.superficie_pausa.blit(texto, rect_texto)

        self.pantalla.blit(self.superficie_pausa, self.rect_pausa)

    def ejecutar_opcion_pausa(self):
        if self.opciones_pausa[self.opcion_seleccionada] == "Reanudar":
            self.pausa = False
        elif self.opciones_pausa[self.opcion_seleccionada] == "Guardar Partida":
            self.guardar_estado("pacman_save.json")
            print("Partida guardada")
        elif self.opciones_pausa[self.opcion_seleccionada] == "Salir":
            exit()


if __name__ == '__main__':
    juego = Controladora()
    juego.empezar()
    while True:
        juego.actualizar()
