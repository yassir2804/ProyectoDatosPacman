import json
import pygame
from pygame.locals import *
from Constantes import *
from Fantasmas import GrupoFantasmas
from Grafo import Grafo
from Pacman import Pacman
from Pellet import GrupoPellets, Pellet, PelletPoder
from Texto import GrupoTexto
from MenuGameOver import MenuGameOver
from Fruta import Fruta
from Vector import Vector1


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

        #
        self.menu_game_over = None
        self.reiniciar_juego = False
        # Crear Pacman primero
        self.pacman = Pacman(self.grafo.obtener_nodo_desde_tiles(14, 32))

        self.casa = self.grafo.crear_nodos_casa(11.5, 14)
        # Conectar con el nodo de la izquierda (columna 9)
        self.grafo.conectar_nodos_casa(self.casa, (12, 14), IZQUIERDA)
        # Conectar con el nodo de la derecha (columna 15)
        self.grafo.conectar_nodos_casa(self.casa, (15, 14), DERECHA)


        # Crear grupo de fantasmas con posiciones específicas
        self.fantasmas = GrupoFantasmas(nodo=self.grafo.obtener_nodo_desde_tiles(13.5, 17), pacman=self.pacman)

        # Configurar posiciones iniciales específicas para cada fantasma
        self.fantasmas.blinky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(13.5, 17))  # Blinky arriba
        self.fantasmas.pinky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(11.5, 17))  # Pinky centro
        self.fantasmas.inky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(15.5, 16))  # Inky izquierda
        self.fantasmas.clyde.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(15.5, 16))  # Clyde derecha



        # Configurar nodo de spawn para todos los fantasmas
        # = self.grafo.obtener_nodo_desde_tiles(13.5, 17)  # Punto de spawn común
        #self.fantasmas.setSpawnNode(nodo_spawn)

        # Inicializar temporizadores para la salida de fantasmas
        self.tiempo_transcurrido = 0
        self.tiempo_entre_fantasmas = 5  # segundos entre cada fantasma
        self.fantasmas_liberados = 0

        # Lista de fantasmas en orden de salida con tiempos específicos
        self.orden_fantasmas = [
            (self.fantasmas.blinky, 0),  # Blinky sale inmediatamente
            (self.fantasmas.pinky, 5),  # Pinky sale a los 5 segundos
            (self.fantasmas.inky, 10),  # Inky sale a los 10 segundos
            (self.fantasmas.clyde, 15)  # Clyde sale a los 15 segundos
        ]

        # Desactivar todos excepto Blinky inicialmente
        self.fantasmas.blinky.activo = True
        self.fantasmas.blinky.en_casa = False
        for fantasma, _ in self.orden_fantasmas[1:]:
            fantasma.activo = False
            fantasma.en_casa = True


        # Grupo de pellets y texto
        self.Pellet = GrupoPellets("mazetest.txt")
        self.grupo_texto = GrupoTexto()
        self.puntaje = 0
        self.tiempo_poder = 0
        self.duracion_poder = 7

        # Frutas
        self.fruta = None
        self.orden_fantasmas = [self.fantasmas.blinky, self.fantasmas.pinky, self.fantasmas.inky, self.fantasmas.clyde]


    def verificacion_pellets(self):  # Añadimos dt como parámetro
        """
        Verifica la colisión con pellets y actualiza el puntaje.
        También maneja la activación del modo freight y los puntos por comer fantasmas.
        """
        # Verificar colisión con pellets
        pellet = self.pacman.comer_pellets(self.Pellet.listaPellets)
        if pellet:
            self.Pellet.numComidos += 1
            if pellet.nombre == PELLETPODER:
                self.puntaje += 50
                self.fantasmas.modo_Freight()
                self.tiempo_poder = self.duracion_poder
                self.power_mode_active = True
            else:
                self.puntaje += 10
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
            self.menu_game_over = MenuGameOver(self.pantalla)

    def reset_nivel(self):
        """Resetea las posiciones de todos los personajes"""
        self.pacman.reset_posicion()
        self.fantasmas.reset()
        self.fantasmas.mostrar()
        # Resetear temporizadores de fantasmas
        self.tiempo_transcurrido = 0
        self.fantasmas_liberados = 0

    def actualizar(self):
        """Método principal de actualización del juego"""
        # Si hay una señal de reinicio, reiniciar el juego
        if self.reiniciar_juego:
            self.reiniciar()
            return
            # Obtener el tiempo delta para actualizaciones consistentes
        dt = self.clock.tick(30) / 1000.0
        if not self.game_over and not self.pausa:  # Añadir verificación de pausa
            if not self.pacman.muerto:


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

            if self.game_over:
                opcion = self.menu_game_over.manejar_evento(event)
                if opcion == "Nuevo Juego":
                    self.reiniciar_juego = True
                    self.game_over = False
                elif opcion == "Salir":
                    exit()
            elif event.type == KEYDOWN:
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

    def reiniciar(self):
        """Reinicia completamente el juego"""
        pygame.init()
        self.fantasmas = GrupoFantasmas(nodo=self.grafo.obtener_nodo_desde_tiles(13.5, 17), pacman=self.pacman)
        self.fantasmas.blinky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(11.5, 17))
        self.fantasmas.clyde.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(15.5, 16))
        self.fantasmas.inky.nodo_inicio(self.grafo.obtener_nodo_desde_tiles(11.5, 17))
        self.Pellet = GrupoPellets("mazetest.txt")
        self.grupo_texto = GrupoTexto()
        self.puntaje = 0
        self.tiempo_poder = 0
        self.game_over = False
        self.menu_game_over = None
        self.reiniciar_juego = False
        self.fruta = None
        self.pacman.reset_vidas()

    def render(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.grafo.render(self.pantalla)
        self.Pellet.render(self.pantalla)
        self.pacman.render(self.pantalla)
        self.fantasmas.render(self.pantalla)
        if self.fruta is not None:
            self.fruta.render(self.pantalla)
        self.grupo_texto.renderizar(self.pantalla)
        if self.game_over:
            self.menu_game_over.dibujar()
        if self.pausa:
            self.dibujar_menu_pausa()
        pygame.display.update()

    def verificar_fruta(self):
        """Verifica eventos relacionados con la fruta"""
        # Crear fruta cuando se hayan comido cierta cantidad de pellets
        if self.Pellet.numComidos == 50 or self.Pellet.numComidos == 140:
            if self.fruta is None:
                self.fruta = Fruta(self.grafo.obtener_nodo_desde_tiles(12, 23))


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
                'direccion': self.pacman.direccion,  # Añadir la dirección actual
                'direccion_deseada': self.pacman.direccion_deseada,
                'blanco': [self.pacman.blanco.posicion.x, self.pacman.blanco.posicion.y] if self.pacman.blanco != self.pacman.nodo else None,
                'vidas': self.pacman.vidas,
                'puntos': self.puntaje
            },
            # Guardar el estado de los fantasmas
            'fantasmas': [
                {
                    'nombre': fantasma.nombre,
                    'posicion': [fantasma.posicion.x, fantasma.posicion.y],
                    'direccion': fantasma.direccion,
                    'modo': {
                        'current': fantasma.modo.current,
                        'tiempo': fantasma.modo.tiempo,
                        'temporizador': fantasma.modo.temporizador
                    },
                    'activo': fantasma.activo,
                    'en_casa': fantasma.en_casa,
                    'duracion_freight': getattr(fantasma, 'duracion_freight', 7),
                    'tiempo_freight': getattr(fantasma, 'tiempo_freight', 0),
                    'parpadeo_freight': getattr(fantasma, 'parpadeo_freight', False),
                    'contador_parpadeo': getattr(fantasma, 'contador_parpadeo', 0),
                    # Guardar la posición del nodo blanco
                    'blanco': [fantasma.blanco.posicion.x, fantasma.blanco.posicion.y] if fantasma.blanco else None
                } for fantasma in self.orden_fantasmas
            ],'fruta':
                {
                    'visible': self.fruta.visible if self.fruta else False,
                    'tiempo': self.fruta.tiempo if self.fruta else 0,
                    'temporizador': self.fruta.temporizador if self.fruta else 0
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

            # Restore Pacman
            self.pacman.posicion = Vector1(estado['pacman']['posicion'][0], estado['pacman']['posicion'][1])
            fila = self.pacman.posicion.y // ALTURACELDA
            columna = self.pacman.posicion.x // ANCHOCELDA
            self.pacman.nodo = self.grafo.obtener_nodo_desde_tiles(columna, fila)
            self.pacman.direccion = estado['pacman']['direccion']  # Restaurar dirección actual
            self.pacman.direccion_deseada = estado['pacman']['direccion_deseada']
            self.pacman.vidas = estado['pacman']['vidas']
            self.puntaje = estado['pacman']['puntos']

            if estado['pacman'].get('blanco'):
                blanco_x, blanco_y = estado['pacman']['blanco']
                blanco_fila = blanco_y // ALTURACELDA
                blanco_columna = blanco_x // ANCHOCELDA
                self.pacman.blanco = self.grafo.obtener_nodo_desde_tiles(blanco_columna, blanco_fila)
            else:
                self.pacman.blanco = self.pacman.nodo

            # Restore ghosts
            for fantasma, datos in zip(self.orden_fantasmas, estado['fantasmas']):
                # Restaurar posición y nodo
                fantasma.posicion = Vector1(datos['posicion'][0], datos['posicion'][1])

                # Calcular nodo basado en la posición
                fila = round(fantasma.posicion.y // ALTURACELDA)
                columna = round(fantasma.posicion.x // ANCHOCELDA)
                fantasma.nodo = self.grafo.obtener_nodo_desde_tiles(columna, fila)

                # Restaurar el nodo blanco
                if 'blanco' in datos and datos['blanco'] is not None:
                    blanco_x, blanco_y = datos['blanco']
                    blanco_fila = round(blanco_y // ALTURACELDA)
                    blanco_columna = round(blanco_x // ANCHOCELDA)
                    fantasma.blanco = self.grafo.obtener_nodo_desde_tiles(blanco_columna, blanco_fila)
                else:
                    fantasma.blanco = fantasma.nodo  # O el valor por defecto que prefieras

                # Restaurar dirección
                if 'direccion' in datos:
                    fantasma.direccion = datos['direccion']

                # Restaurar modo y estados
                fantasma.modo.current = datos['modo']['current']
                fantasma.modo.tiempo = datos['modo']['tiempo']
                fantasma.modo.temporizador = datos['modo']['temporizador']
                fantasma.activo = datos['activo']
                fantasma.en_casa = datos['en_casa']

                # Restaurar estados de freight
                fantasma.duracion_freight = datos.get('duracion_freight', 7)
                fantasma.tiempo_freight = datos.get('tiempo_freight', 0)
                fantasma.parpadeo_freight = datos.get('parpadeo_freight', False)
                fantasma.contador_parpadeo = datos.get('contador_parpadeo', 0)

                # Manejar el modo FREIGHT específicamente
                if fantasma.modo.current == FREIGHT:
                    if fantasma.modo.tiempo is None:
                        fantasma.modo.tiempo = fantasma.duracion_freight
                    if fantasma.modo.temporizador is None:
                        fantasma.modo.temporizador = 0

            # Restore fruit
            if estado['fruta']['visible']:
                self.fruta = Fruta(self.grafo.obtener_nodo_desde_tiles(12, 23))
                self.fruta.visible = estado['fruta']['visible']
                self.fruta.tiempo = estado['fruta']['tiempo']
                self.fruta.temporizador = estado['fruta']['temporizador']
            else:
                self.fruta = None

            # Restore pellets
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

            # Update UI
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

    def set_initial_positions(self):
        self.pacman.posicion = self.grafo.punto_partida_pacman()
        self.fantasmas.blinky.posicion = self.grafo.obtener_nodo_desde_tiles(16, 16).posicion
        self.fantasmas.clyde.posicion = self.grafo.obtener_nodo_desde_tiles(21, 18).posicion
        self.fantasmas.inky.posicion = self.grafo.obtener_nodo_desde_tiles(19, 17).posicion
        self.fantasmas.pinky.posicion = self.grafo.obtener_nodo_desde_tiles(18, 16).posicion


if __name__ == '__main__':
    juego = Controladora()
    juego.empezar()
    while True:
        juego.actualizar()
