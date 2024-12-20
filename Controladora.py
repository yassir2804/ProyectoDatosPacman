import json
import pygame
from pygame.locals import *
from Constantes import *
from Fantasmas import GrupoFantasmas
from Grafo import Grafo
from LevelManager import LevelManager
from MapaVisual import MapaRenderer
from Pacman import Pacman
from Pellet import GrupoPellets, Pellet, PelletPoder
from Texto import GrupoTexto
from MenuGameOver import MenuGameOver
from Fruta import Fruta
from TextoTemporal import TextoTemporal
from Vector import Vector1


class Controladora(object):
    """
    Clase principal que controla el flujo del juego Pac-Man.
    Maneja la inicialización, actualización y renderizado de todos los elementos del juego.
    """

    def __init__(self):
        """
        Inicializa todos los componentes necesarios para el juego.
        Configura la ventana, el mapa, los personajes y los elementos de juego.
        """
        # Inicialización de pygame y ventana
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMANIOPANTALLA, 0, 32)
        self.fondo = None
        self.clock = pygame.time.Clock()

        # Inicialización del mapa y sus elementos
        self.grafo = Grafo("mazetest.txt")
        self.grafo.set_portales((0, 17), (27, 17))  # Configurar túneles
        self.mapa_renderer = MapaRenderer()
        self.mapa_renderer.cargar_mapa("mazetest.txt")

        # Estados del juego
        self.game_over = False
        self.pausa = False
        self.reiniciar_juego = False
        self.game_over_ganado = False

        # Inicialización de Pac-Man
        self.pacman = Pacman(self.grafo.obtener_nodo_desde_tiles(14, 26))

        # Configuración inicial del juego
        self.configurar_casa_fantasmas()
        self.inicializar_fantasmas()
        self.configurar_audio()
        self.inicializar_elementos_juego()
        self.denegar_accesos()

    def configurar_casa_fantasmas(self):
        """
        Configura la casa de los fantasmas y establece sus conexiones en el grafo.
        """
        self.casa = self.grafo.crear_nodos_casa(11.5, 14)
        self.grafo.conectar_nodos_casa(self.casa, (12, 14), IZQUIERDA)
        self.grafo.conectar_nodos_casa(self.casa, (15, 14), DERECHA)

    def inicializar_fantasmas(self):
        """
        Inicializa el grupo de fantasmas y configura sus posiciones iniciales.
        """
        # Crear grupo de fantasmas con nodo de spawn común
        nodo_spawn = self.grafo.obtener_nodo_desde_tiles(13.5, 17)
        self.fantasmas = GrupoFantasmas(nodo=nodo_spawn, pacman=self.pacman)

        # Configurar posiciones iniciales de cada fantasma
        self.fantasmas.blinky.set_nodo_inicio(self.grafo.obtener_nodo_desde_tiles(13.5, 14))
        self.fantasmas.pinky.set_nodo_inicio(self.grafo.obtener_nodo_desde_tiles(13.5, 17))
        self.fantasmas.inky.set_nodo_inicio(self.grafo.obtener_nodo_desde_tiles(11.5, 17))
        self.fantasmas.clyde.set_nodo_inicio(self.grafo.obtener_nodo_desde_tiles(15.5, 17))

        # Establecer punto de spawn común
        self.fantasmas.set_nodo_spawn(nodo_spawn)

    def configurar_audio(self):
        """
        Configura los efectos de sonido utilizados en el juego.
        """
        self.sonido_reinicio = pygame.mixer.Sound("multimedia/levelup.wav")
        self.sonido_sirena = pygame.mixer.Sound("multimedia/sonidosirena.wav")

    def inicializar_elementos_juego(self):
        """
        Inicializa los elementos básicos del juego como pellets, textos y contadores.
        """
        self.Pellet = GrupoPellets("mazetest.txt")
        self.grupo_texto = GrupoTexto()
        self.level_manager = LevelManager()
        self.menu_game_over = MenuGameOver(self.pantalla)

        # Contadores y temporizadores
        self.puntaje = 0
        self.tiempo_poder = 0
        self.duracion_poder = 7

        # Elementos adicionales
        self.fruta = None
        self.textos_temporales = []
        self.fuente_pausa = None

    def configurarFuente(self, ruta_fuente, tamanio):
        """
        Configura la fuente utilizada en el menú de pausa.

        Args:
            ruta_fuente (str): Ruta al archivo de la fuente
            tamanio (int): Tamaño de la fuente
        """
        self.fuente_pausa = pygame.font.Font(ruta_fuente, tamanio)

    def verificar_fruta(self):
        """
        Maneja la aparición y colisión con frutas durante el juego.
        """
        # Crear fruta en momentos específicos
        if self.Pellet.numComidos in [50, 140] and self.fruta is None:
            self.fruta = Fruta(self.grafo.obtener_nodo_desde_tiles(13, 20), self.level_manager.nivel_actual)

        if self.fruta is not None:
            if self.pacman.colision_fruta(self.fruta):
                self.manejar_colision_fruta()
            elif self.fruta.desaparecer:
                self.fruta = None

    def verificacion_pellets(self):
        """
        Verifica la colisión de Pacman con los pellets y actualiza el estado del juego.
        - Maneja el puntaje
        - Activa el modo de poder
        - Controla la liberación de fantasmas
        - Verifica si se completó el nivel
        """
        pellet = self.pacman.comer_pellets(self.Pellet.listaPellets)
        if pellet:
            self.Pellet.numComidos += 1
            # Si es un pellet de poder
            if pellet.nombre == PELLETPODER:
                self.puntaje += 50
                self.fantasmas.modo_Freight()
                self.tiempo_poder = self.duracion_poder
            else:
                self.puntaje += 10

            # Actualizar puntaje y eliminar pellet
            self.grupo_texto.actualizar_puntaje(self.puntaje)
            self.Pellet.listaPellets.remove(pellet)

            # Liberar fantasmas según pellets comidos
            if self.Pellet.numComidos == 30:
                self.fantasmas.inky.nodo_inicio.dar_acceso(DERECHA, self.fantasmas.inky)
            if self.Pellet.numComidos == 70:
                self.fantasmas.clyde.nodo_inicio.dar_acceso(IZQUIERDA, self.fantasmas.clyde)

            # Verificar si se completó el nivel
            if self.level_manager.verificar_nivel_completado(self.Pellet):
                if self.level_manager.subir_nivel():
                    # Actualizar texto del nivel
                    self.grupo_texto.todos_los_textos[LEVELTXT].set_texto(str(self.level_manager.nivel_actual).zfill(3))
                    self.reiniciar_nivel()
                else:
                    # Victoria del juego (después del nivel 3)
                    self.game_over_ganado = True
                    pygame.mixer.stop()
                    self.mostrar_pantalla_victoria()

    def verificar_vidas(self):
        """
        Verifica el estado de las vidas y maneja el game over.
        - Controla colisiones con fantasmas
        - Actualiza el puntaje y vidas
        - Maneja el estado de game over
        """
        # Verificar colisiones con fantasmas
        puntos = self.pacman.colision_con_fantasmas(self.fantasmas, self.grafo, self.textos_temporales)
        if puntos > 0:
            self.puntaje += puntos
            self.grupo_texto.actualizar_puntaje(self.puntaje)

        # Actualizar display de vidas
        self.grupo_texto.actualizar_vidas(self.pacman.vidas)

        # Verificar game over
        if self.pacman.vidas <= 0 and not self.game_over:
            self.game_over = True
            self.fantasmas.esconder()

    def verificar_eventos(self):
        """
        Maneja los eventos del juego (teclado, cierre de ventana, etc.)
        - Procesa eventos de pygame
        - Maneja estados de game over y pausa
        - Controla sonidos del juego
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if self.game_over:
                self.manejar_eventos_game_over(event)
            elif event.type == KEYDOWN:
                self.manejar_eventos_teclado(event)

        # Mantener sonido de sirena
        if not pygame.mixer.get_busy():
            self.sonido_sirena.set_volume(0.5)
            self.sonido_sirena.play(-1)

    def verificar_fatasmas(self):
        """
        Verifica colisiones entre Pacman y los fantasmas en modo vulnerable
        """
        for fantasma in self.fantasmas:
            if self.pacman.colision_fruta(fantasma):
                if fantasma.modo.current is FREIGHT:
                    fantasma.iniciar_spawn()

    def actualizar(self):
        """
        Metodo principal de actualización del juego.
        Maneja la lógica principal del bucle del juego.
        """
        # Verificar señal de reinicio
        if self.reiniciar_juego:
            self.reiniciar()
            return

        dt = self.clock.tick(30) / 1000.0
        if not self.game_over and not self.pausa:
            self.mapa_renderer.actualizar(dt, self.fantasmas.modo_freight_activo())

            if not self.pacman.muerto:
                # Actualizar elementos del juego
                self.pacman.actualizar(dt)
                self.fantasmas.actualizar(dt)
                self.Pellet.actualizar(dt)
                if self.fruta is not None:
                    self.fruta.actualizar(dt)

                self.verificacion_pellets()
            else:
                # Actualizar estado cuando Pacman está muerto
                self.grupo_texto.actualizar(dt)
                self.verificar_vidas()
                self.verificar_eventos()
                self.verificar_fruta()

                self.pacman.actualizar(dt)
                if self.pacman.animacion_muerte_terminada():
                    self.reiniciar_nivel()

            # Actualizaciones generales
            self.grupo_texto.actualizar(dt)
            self.verificar_vidas()
            self.verificar_eventos()
            self.verificar_fruta()

            # Actualizar textos temporales
            self.textos_temporales = [texto for texto in self.textos_temporales if texto.actualizar()]

            self.render()
        else:
            self.verificar_eventos()
            self.render()

    def reiniciar_nivel(self):
        """Reinicia el nivel actual dependiendo si es por muerte o por paso de nivel"""
        # Detener sonidos

        if self.level_manager.verificar_nivel_completado(self.Pellet):
            # Caso 1: Paso de nivel
            self.reiniciar_por_nuevo_nivel()
        else:
            # Caso 2: Muerte de Pacman
            self.reiniciar_por_muerte()

    def reiniciar_por_nuevo_nivel(self):
        """Reinicia el nivel cuando se pasa a uno nuevo"""
        # Resetear posiciones
        for fantasma in self.fantasmas:
            fantasma.modo.current = SCATTER

        pygame.mixer.stop()
        self.pacman.reset_posicion()
        self.fantasmas.reset()
        self.fantasmas.actualizar_velocidades_nivel(self.level_manager.nivel_actual)
        self.inicializar_fantasmas()

        # Actualizar elementos visuales

        self.mapa_renderer.color_mapa(self.level_manager.nivel_actual)
        self.Pellet = GrupoPellets("mazetest.txt")

        # Actualizar velocidad de fantasmas para el nuevo nivel
        nueva_velocidad = self.level_manager.obtener_velocidad_fantasmas()
        for fantasma in self.fantasmas:
            fantasma.velocidad = nueva_velocidad
            fantasma.velocidad_base = nueva_velocidad
            fantasma.modo.current = SCATTER
            fantasma.actualizar_skin()

        self.denegar_accesos()
        self.mostrar_pantalla_nivel()

    def reiniciar_por_muerte(self):
        """Reinicia el nivel cuando Pacman muere"""

        # Actualizar velocidad de fantasmas para el nuevo nivel
        nueva_velocidad = self.level_manager.obtener_velocidad_fantasmas()
        for fantasma in self.fantasmas:
            fantasma.velocidad = nueva_velocidad
            fantasma.modo.current = SCATTER
            fantasma.actualizar_skin()

        # Resetear posiciones
        self.pacman.direccion = STOP
        self.verificar_vidas()

        # self.pacman.reset_posicion()
        self.fantasmas.reset()

    def mostrar_pantalla_victoria(self):
        """Muestra la pantalla de victoria cuando se completa el juego"""
        tiempo_inicio = pygame.time.get_ticks()
        font_grande = pygame.font.Font("Fuentes/PressStart2P-Regular.ttf", 50)
        font_pequeña = pygame.font.Font("Fuentes/PressStart2P-Regular.ttf", 36)
        sonido_victoria = pygame.mixer.Sound("multimedia/Efecto de Sonido de Victoria Plantas Vs  Zombies.mp3")

        # Calculamos el tamaño disponible para la imagen
        altura_imagen = int(TAMANIOPANTALLA[1] * 0.3)
        tamanio_imagen = (altura_imagen, altura_imagen)

        # Cargar y escalar la imagen al tamaño calculado
        imagen_victoria = pygame.image.load("multimedia/premiesito.png")
        imagen_victoria = pygame.transform.scale(imagen_victoria, tamanio_imagen)

        # Crear los textos
        texto_victoria = font_pequeña.render("¡HAS GANADO!", True, (255, 255, 0))
        texto_tu_premio = font_pequeña.render("TU PREMIO ES", True, (255, 255, 0))

        # Calculamos las posiciones para una distribución proporcional
        espacio_vertical = TAMANIOPANTALLA[1] // 6

        # Ajustamos las posiciones - victoria arriba, imagen en medio, premio abajo
        rect_victoria = texto_victoria.get_rect(center=(TAMANIOPANTALLA[0] // 2, espacio_vertical * 1.5))
        rect_imagen = imagen_victoria.get_rect(center=(TAMANIOPANTALLA[0] // 2, espacio_vertical * 3))
        rect_tu_premio = texto_tu_premio.get_rect(center=(TAMANIOPANTALLA[0] // 2, espacio_vertical * 4.5))

        sonido_victoria.play()
        while pygame.time.get_ticks() - tiempo_inicio < 5000:  # 5 segundos
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            # Renderizar fondo negro
            self.pantalla.fill(NEGRO)
            # Overlay semitransparente
            s = pygame.Surface(TAMANIOPANTALLA)
            s.set_alpha(128)
            s.fill(NEGRO)
            self.pantalla.blit(s, (0, 0))

            # Mostrar textos e imagen en el nuevo orden
            self.pantalla.blit(texto_victoria, rect_victoria)
            self.pantalla.blit(imagen_victoria, rect_imagen)
            self.pantalla.blit(texto_tu_premio, rect_tu_premio)

            pygame.display.update()
            self.clock.tick(30)

        # Al finalizar la pantalla de victoria, activar game over
        self.game_over = True

    def mostrar_pantalla_nivel(self):
        """Muestra la pantalla de transición entre niveles"""
        tiempo_inicio = pygame.time.get_ticks()
        font = pygame.font.Font("Fuentes/PressStart2P-Regular.ttf", 74)
        sonido_pasa_nivel = pygame.mixer.Sound("multimedia/efecto de sonido victoria happy wheels.mp3")
        texto_nivel = font.render(f"NIVEL {self.level_manager.nivel_actual}", True, (255, 255, 0))
        rect_texto = texto_nivel.get_rect(center=(TAMANIOPANTALLA[0] // 2, TAMANIOPANTALLA[1] // 2))

        while pygame.time.get_ticks() - tiempo_inicio < 5000:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            # Renderizar pantalla de nivel
            self.pantalla.fill(NEGRO)

            # Overlay semitransparente
            s = pygame.Surface(TAMANIOPANTALLA)
            s.set_alpha(128)
            s.fill(NEGRO)
            self.pantalla.blit(s, (0, 0))

            # Mostrar texto del nivel
            self.pantalla.blit(texto_nivel, rect_texto)
            sonido_pasa_nivel.play()
            pygame.display.update()
            self.clock.tick(30)
    def set_fondo(self):
        self.fondo = pygame.surface.Surface(TAMANIOPANTALLA).convert()
        self.fondo.fill(NEGRO)

    def empezar(self):
        self.set_fondo()
        #self.denegar_accesos()

    def denegar_accesos(self):
        self.grafo.denegar_acceso_a_casa(self.pacman)
        self.grafo.denegar_acceso_a_casa_entidades(self.fantasmas)
        self.grafo.denegar_acceso_entidades(13.5, 17, IZQUIERDA, self.fantasmas)
        self.grafo.denegar_acceso_entidades(2 + 11.5, 3 + 14, DERECHA, self.fantasmas)
        self.fantasmas.inky.nodo_inicio.denegar_acceso(DERECHA, self.fantasmas.inky)
        self.fantasmas.clyde.nodo_inicio.denegar_acceso(IZQUIERDA, self.fantasmas.clyde)

    def manejar_eventos_game_over(self, event):
        """Maneja los eventos durante la pantalla de game over"""
        opcion = self.menu_game_over.manejar_evento(event)
        if opcion == "Nuevo Juego":
            self.reiniciar_juego = True
            self.game_over = False
        elif opcion == "Salir":
            exit()

    def manejar_eventos_teclado(self, event):
        """Maneja los eventos de teclado"""
        if event.key == K_ESCAPE:
            if not self.pausa:
                self.crear_menu_pausa()
            else:
                self.pausa = False
        elif self.pausa:
            self.manejar_eventos_pausa(event)

    def reiniciar(self):
        """Reinicia completamente el juego"""
        pygame.init()

        for fantasma in self.fantasmas:
            fantasma.modo.current = SCATTER

        self.pacman.direccion = STOP
        self.denegar_accesos()
        self.inicializar_fantasmas()

        # Reiniciar estado de fantasmas
        self.fantasmas.reset()
        self.fantasmas.mostrar()

        # Reiniciar elementos del juego
        self.Pellet = GrupoPellets("mazetest.txt")
        self.puntaje = 0
        self.tiempo_poder = 0
        self.game_over = False
        self.menu_game_over = MenuGameOver(self.pantalla)
        self.reiniciar_juego = False
        self.level_manager.nivel_actual=1
        self.fruta = None
        self.pacman.reset_vidas()
        self.grupo_texto = GrupoTexto()
        self.mapa_renderer.color_mapa(1)

    def render(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.mapa_renderer.render(self.pantalla)
        self.Pellet.render(self.pantalla)
        self.pacman.render(self.pantalla)
        self.fantasmas.render(self.pantalla)

        if self.fruta is not None:
            self.fruta.render(self.pantalla)
        self.grupo_texto.renderizar(self.pantalla)
        for texto in self.textos_temporales:
            texto.render(self.pantalla)
        if self.game_over:
            self.menu_game_over.dibujar(self.game_over_ganado)
        if self.pausa:
            self.dibujar_menu_pausa()
        pygame.display.update()


    def manejar_colision_fruta(self):
        """Maneja la colisión con una fruta"""
        pos_x = int(self.fruta.posicion.x - 20)
        pos_y = int(self.fruta.posicion.y - 20)
        puntos_fruta = self.fruta.puntos

        # Crear texto temporal de puntos
        texto = TextoTemporal(
            texto=str(puntos_fruta),
            posicion=(pos_x, pos_y),
            duracion=1000,
            fuente=pygame.font.Font(None, 20),
            color=(255, 255, 255)
        )
        self.textos_temporales.append(texto)

        # Actualizar puntaje
        self.puntaje += puntos_fruta
        self.grupo_texto.actualizar_puntaje(self.puntaje)
        self.fruta = None

    def configurar_nivel_cargado(self):
        """
        Configura todos los elementos necesarios para el nivel actual cuando se carga una partida.
        Incluye color del mapa, velocidad de fantasmas y textos UI.
        """
        # Actualizar color del mapa según el nivel
        self.mapa_renderer.color_mapa(self.level_manager.nivel_actual)

        if self.Pellet.numComidos >= 30:
            self.fantasmas.inky.nodo_inicio.dar_acceso(DERECHA, self.fantasmas.inky)
        if self.Pellet.numComidos >= 70:
            self.fantasmas.clyde.nodo_inicio.dar_acceso(IZQUIERDA, self.fantasmas.clyde)

        # Actualizar velocidades de fantasmas para el nivel actual
        nueva_velocidad = self.level_manager.obtener_velocidad_fantasmas()
        for fantasma in self.fantasmas:
            fantasma.velocidad = nueva_velocidad
            fantasma.velocidad_base = nueva_velocidad

        # Actualizar textos en la UI
        self.grupo_texto.todos_los_textos[LEVELTXT].set_texto(str(self.level_manager.nivel_actual).zfill(3))
        self.grupo_texto.actualizar_puntaje(self.puntaje)
        self.grupo_texto.actualizar_vidas(self.pacman.vidas)

    def guardar_estado(self, archivo):
        # Crear diccionario con meto do el estado del juego
        estado = {
            # Almacenar estado de Pac-man
            'pacman': {
                'posicion': [self.pacman.posicion.x, self.pacman.posicion.y],
                'direccion': self.pacman.direccion,  # Dirección actual de movimiento
                'direccion_deseada': self.pacman.direccion_deseada,
                # Guardar posición del nodo objetivo si es diferente al nodo actual
                'blanco': [self.pacman.blanco.posicion.x,
                           self.pacman.blanco.posicion.y] if self.pacman.blanco != self.pacman.nodo else None,
                'vidas': self.pacman.vidas,
                'puntos': self.puntaje
            },
            # Guardar estado de cada fantasma
            'fantasmas': [
                {
                    'nombre': fantasma.nombre,
                    'posicion': [fantasma.posicion.x, fantasma.posicion.y],
                    'direccion': fantasma.direccion,
                    'modo': {
                        'current': fantasma.modo.current,  # Modo actual del fantasma (SCATTER, CHASE, etc)
                        'tiempo': fantasma.modo.tiempo,
                        'temporizador': fantasma.modo.temporizador
                    },
                    # Estados relacionados con el modo vulnerable (FREIGHT)
                    'duracion_freight': getattr(fantasma, 'duracion_freight', 7),
                    'tiempo_freight': getattr(fantasma, 'tiempo_freight', 0),
                    'parpadeo_freight': getattr(fantasma, 'parpadeo_freight', False),
                    'contador_parpadeo': getattr(fantasma, 'contador_parpadeo', 0),
                    # Guardar nodo objetivo del fantasma
                    'blanco': [fantasma.blanco.posicion.x, fantasma.blanco.posicion.y] if fantasma.blanco else None
                } for fantasma in self.fantasmas
            ], 'fruta':
                {
                    'visible': self.fruta.visible if self.fruta else False,
                    'tiempo': self.fruta.tiempo if self.fruta else 0,
                    'temporizador': self.fruta.temporizador if self.fruta else 0
                },
            # Guardar estado de los pellets en el tablero
            'pellets': [
                {
                    'fila': pellet.posicion.y // ALTURACELDA,
                    'columna': pellet.posicion.x // ANCHOCELDA,
                    'tipo': pellet.nombre,

                } for pellet in self.Pellet.listaPellets
            ],
            'tiempo_poder': self.tiempo_poder,
            'nivel': self.level_manager.nivel_actual
            , 'velocidad': self.level_manager.velocidad_base_fantasmas,
            'pellets_comidos': self.Pellet.numComidos  # Contador de pellets comidos
        }
        # Intentar guardar el estado en archivo JSON
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
            # Leer el archivo JSON con el estado guardado
            with open(archivo, 'r', encoding='utf-8') as f:
                estado = json.load(f)

            # Restaurar estado de Pac-man
            self.pacman.posicion = Vector1(estado['pacman']['posicion'][0], estado['pacman']['posicion'][1])
            fila = self.pacman.posicion.y // ALTURACELDA
            columna = self.pacman.posicion.x // ANCHOCELDA
            self.pacman.nodo = self.grafo.obtener_nodo_desde_tiles(columna, fila)
            self.pacman.direccion = estado['pacman']['direccion']
            self.pacman.direccion_deseada = estado['pacman']['direccion_deseada']
            self.pacman.vidas = estado['pacman']['vidas']
            self.puntaje = estado['pacman']['puntos']

            # Restaurar nodo objetivo de Pac-man
            if estado['pacman'].get('blanco'):
                blanco_x, blanco_y = estado['pacman']['blanco']
                blanco_fila = blanco_y // ALTURACELDA
                blanco_columna = blanco_x // ANCHOCELDA
                self.pacman.blanco = self.grafo.obtener_nodo_desde_tiles(blanco_columna, blanco_fila)
            else:
                self.pacman.blanco = self.pacman.nodo

            # Restaurar estado de los fantasmas
            for fantasma, datos in zip(self.fantasmas, estado['fantasmas']):
                # Restaurar posición y obtener nodo correspondiente
                fantasma.posicion = Vector1(datos['posicion'][0], datos['posicion'][1])
                fila = fantasma.posicion.y // ALTURACELDA
                columna = fantasma.posicion.x // ANCHOCELDA
                fantasma.nodo = self.grafo.obtener_nodo_desde_tiles(columna, fila)

                # Manejar caso de nodo nulo asignando posición por defecto según el fantasma
                if fantasma.nodo is None:
                    if fantasma.nombre == 98:  # Blinky
                        fantasma.nodo = self.grafo.obtener_nodo_desde_tiles(15.5, 17)
                    if fantasma.nombre == 97:  # Pinky
                        fantasma.nodo = self.grafo.obtener_nodo_desde_tiles(13.5, 17)
                    if fantasma.nombre == 96:  # Inky/Clyde
                        fantasma.nodo = self.grafo.obtener_nodo_desde_tiles(11.5, 17)

                # Restaurar nodo objetivo del fantasma
                if 'blanco' in datos and datos['blanco'] is not None:
                    blanco_x, blanco_y = datos['blanco']
                    blanco_fila = blanco_y // ALTURACELDA
                    blanco_columna = blanco_x // ANCHOCELDA
                    fantasma.blanco = self.grafo.obtener_nodo_desde_tiles(blanco_columna, blanco_fila)
                else:
                    fantasma.blanco = fantasma.nodo  # Si no hay blanco, usar nodo actual

                # Manejar caso de nodo objetivo nulo
                if fantasma.blanco is None:
                    if fantasma.nombre == 98:
                        fantasma.blanco = self.grafo.obtener_nodo_desde_tiles(15.5, 16)
                    if fantasma.nombre == 97:
                        fantasma.blanco = self.grafo.obtener_nodo_desde_tiles(13.5, 16)
                    if fantasma.nombre == 96:
                        fantasma.blanco = self.grafo.obtener_nodo_desde_tiles(11.5, 16)

                # Restaurar dirección del fantasma
                if 'direccion' in datos:
                    fantasma.direccion = datos['direccion']

                # Restaurar modo y estados del fantasma
                fantasma.modo.current = datos['modo']['current']
                fantasma.modo.tiempo = datos['modo']['tiempo']
                fantasma.modo.temporizador = datos['modo']['temporizador']

                # Restaurar estados del modo vulnerable (FREIGHT)
                fantasma.duracion_freight = datos.get('duracion_freight', 7)
                fantasma.tiempo_freight = datos.get('tiempo_freight', 0)
                fantasma.parpadeo_freight = datos.get('parpadeo_freight', False)
                fantasma.contador_parpadeo = datos.get('contador_parpadeo', 0)

                # Configurar tiempo del modo FREIGHT si es necesario
                if fantasma.modo.current == FREIGHT:
                    if fantasma.modo.tiempo is None:
                        fantasma.modo.tiempo = fantasma.duracion_freight
                    if fantasma.modo.temporizador is None:
                        fantasma.modo.temporizador = 0

                # Dar acceso a la casa si está en modo SPAWN
                if fantasma.modo.current == SPAWN:
                    self.grafo.dar_acceso_a_casa(fantasma)

            # Restaurar estado de los pellets
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

            self.Pellet.numComidos = estado.get('pellets_comidos', 0)

            # Restaurar estado del nivel
            self.tiempo_poder = estado['tiempo_poder']
            self.level_manager.nivel_actual = estado['nivel']
            self.level_manager.velocidad_base_fantasmas = estado['velocidad']

            # Actualizar interfaz de usuario si existe
            if hasattr(self, 'grupo_texto'):
                self.grupo_texto.actualizar_puntaje(self.puntaje)
                self.grupo_texto.actualizar_vidas(self.pacman.vidas)

            # Restaurar estado de la fruta
            if estado['fruta']['visible']:
                self.fruta = Fruta(self.grafo.obtener_nodo_desde_tiles(13, 20), self.level_manager.nivel_actual)
                self.fruta.visible = estado['fruta']['visible']
                self.fruta.tiempo = estado['fruta']['tiempo']
                self.fruta.temporizador = estado['fruta']['temporizador']
            else:
                self.fruta = None

            # Configurar nivel después de cargar el estado
            self.configurar_nivel_cargado()

            return True
        except Exception as e:
            print(f"Error al cargar el estado: {str(e)}")
            return False

    def crear_menu_pausa(self):
        # Activar el estado de pausa
        self.pausa = True

        # Definir las opciones disponibles en el menú de pausa
        self.opciones_pausa = ["Reanudar", "Guardar Partida", "Salir"]

        # Inicializar la opción seleccionada en 0 (primera opción)
        self.opcion_seleccionada = 0

        # Cargar la fuente personalizada si aún no está cargada
        if self.fuente_pausa is None:
            self.configurarFuente("Fuentes/PressStart2P-Regular.ttf", 20)  # Usa la fuente PressStart2P en tamaño 20

        # Definir dimensiones del menú de pausa
        ANCHO_MENU = 320  # Ancho en píxeles del menú
        ALTO_MENU = 200  # Alto en píxeles del menú

        # Crear superficie para el menú de pausa
        self.superficie_pausa = pygame.Surface((ANCHO_MENU, ALTO_MENU))
        self.superficie_pausa.fill(NEGRO)  # Rellenar el fondo con color negro

        # Obtener el rectángulo de la superficie para posicionar el menú
        self.rect_pausa = self.superficie_pausa.get_rect()

        # Centrar el menú en la pantalla
        self.rect_pausa.center = (TAMANIOPANTALLA[0] // 2, TAMANIOPANTALLA[1] // 2)

    def manejar_eventos_pausa(self, event):
        """Maneja los eventos durante la pausa"""
        if event.key == K_UP:
            self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones_pausa)
        elif event.key == K_DOWN:
            self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones_pausa)
        elif event.key == K_RETURN:
            self.ejecutar_opcion_pausa()
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

        # Dibujar opciones usando la fuente personalizada
        for i, opcion in enumerate(self.opciones_pausa):
            color = (255, 255, 0) if i == self.opcion_seleccionada else (255, 255, 255)
            texto = self.fuente_pausa.render(opcion, True, color)
            rect_texto = texto.get_rect()
            rect_texto.centerx = self.superficie_pausa.get_width() // 2
            rect_texto.y = 50 + i * 50
            self.superficie_pausa.blit(texto, rect_texto)

        self.pantalla.blit(self.superficie_pausa, self.rect_pausa)

    def ejecutar_opcion_pausa(self):
        #Aqui simplemente manejamos las opciones del menu de pausa
        if self.opciones_pausa[self.opcion_seleccionada] == "Reanudar":
            self.pausa = False
        elif self.opciones_pausa[self.opcion_seleccionada] == "Guardar Partida":
            self.guardar_estado("pacman_save.json")
            print("Partida guardada")
        elif self.opciones_pausa[self.opcion_seleccionada] == "Salir":
            exit()
