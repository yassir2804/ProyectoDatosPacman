import pygame
from pygame.locals import *
from Constantes import *
from Grafo import Grafo
from Pacman import Pacman
from Pellet import GrupoPellets
from Texto import GrupoTexto
from Fantasmas import GrupoFantasmas
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
        self.fantasmas.clyde.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(16, 16))
        self.fantasmas.inky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(16, 20))
        self.fantasmas.pinky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(18, 16))

        # Grupo de pellets y texto
        self.Pellet = GrupoPellets("mazetest.txt")
        self.grupo_texto = GrupoTexto()
        self.puntaje = 0
        self.tiempo_poder = 0
        self.duracion_poder = 7

        #Frutas
        self.fruta = None


    def verificacion_pellets(self):
        pellet = self.pacman.comer_pellets(self.Pellet.listaPellets)
        if pellet:
            self.Pellet.numComidos += 1
            if pellet.nombre == PELLETPODER:
                self.puntaje += 50  # Más puntos por power pellet
                self.fantasmas.modo_Freight()
                self.tiempo_poder = self.duracion_poder
            else:
                self.puntaje += 10  # Puntos normales por pellet regular
            self.grupo_texto.actualizarPuntaje(self.puntaje)
            self.Pellet.listaPellets.remove(pellet)

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

    def actualizar(self):
        if not self.game_over:
            dt = self.clock.tick(30) / 1000.0

            if not self.pacman.muerto:
                self.pacman.actualizar(dt)
                self.fantasmas.actualizar(dt)
                self.Pellet.actualizar(dt)
                if self.fruta is not None:
                    self.fruta.actualizar(dt)
                    
                self.verificacion_pellets()
            else:
                # Si Pacman está muerto, solo actualizar su timer
                self.pacman.actualizar(dt)
                # Cuando termina el timer, reset del nivel
                if not self.pacman.muerto:
                    self.reset_nivel()

            self.grupo_texto.actualizar(dt)
            self.verificar_vidas()
            self.verificar_eventos()
            self.verificar_fruta()
            self.render()
        else:
            # En game over, solo procesar eventos para salir
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

    def render(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.grafo.render(self.pantalla)
        self.Pellet.render(self.pantalla)
        self.pacman.render(self.pantalla)
        self.fantasmas.render(self.pantalla)
        if self.fruta is not None:
            self.fruta.render(self.pantalla)
        self.grupo_texto.renderizar(self.pantalla)
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


if __name__ == '__main__':
    juego = Controladora()
    juego.empezar()
    while True:
        juego.actualizar()
