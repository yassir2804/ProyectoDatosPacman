import pygame
from pygame.locals import *
from Constantes import *
from Grafo import Grafo
from Pacman import Pacman
from Pellet import GrupoPellets
from Texto import GrupoTexto
from Fantasmas import GrupoFantasmas


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
        if not self.game_over:
            dt = self.clock.tick(30) / 1000.0

            if not self.pacman.muerto:
                self.actualizar_temporizador_fantasmas(dt)  # Añadir esta línea
                self.pacman.actualizar(dt)
                self.fantasmas.actualizar(dt)
                self.Pellet.actualizar(dt)
                self.verificacion_pellets()
            else:
                # Si Pacman está muerto, solo actualizar su timer
                self.pacman.actualizar(dt)
                # Cuando termina el timer, reset del nivel
                if not self.pacman.muerto:
                    self.reset_nivel()

            self.grupo_texto.actualizar(dt)
            self.verificar_vidas()
            self.verificarEventos()
            self.render()
        else:
            # En game over, solo procesar eventos para salir
            self.verificarEventos()
            self.render()

    def setFondo(self):
        self.fondo = pygame.surface.Surface(TAMANIOPANTALLA).convert()
        self.fondo.fill(NEGRO)

    def empezar(self):
        self.setFondo()

    def verificarEventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.grafo.render(self.pantalla)
        self.Pellet.render(self.pantalla)
        self.pacman.render(self.pantalla)
        self.fantasmas.render(self.pantalla)
        self.grupo_texto.renderizar(self.pantalla)
        pygame.display.update()

if __name__ == '__main__':
    juego = Controladora()
    juego.empezar()
    while True:
        juego.actualizar()
