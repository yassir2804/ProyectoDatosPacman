import pygame
from pygame.locals import *

from TextoTemporal import TextoTemporal
from Vector import Vector1
from Constantes import *
from Entidad import Entidad


class Pacman(Entidad):
    def __init__(self, nodo):
        super().__init__(nodo)  # Llamada al constructor de la clase padre
        self.animacion_muerte_completa = True
        self.nombre = PACMAN
        self.color = AMARILLO
        self.direccion = STOP
        self.direccion_deseada = STOP
        self.tiene_poder = False
        self.tiempo_poder = 0
        self.duracion_poder = 7
        self.fantasmas = []
        # Variables para el sistema de vidas
        self.vidas = 3
        self.muerto = False
        self.tiempo_muerte = 0
        self.duracion_muerte = 3  # 3 segundos de pausa al morir
        self.nodo_inicial = nodo  # Guardar nodo inicial para resetear posición
        self.porcentaje_entre_nodos = 0.0  # Nueva variable para tracking

        # Inicialización de la animación
        self.cargar_animaciones()
        self.skin = self.skins[DERECHA][0]  # Imagen inicial

        # Variables para el control del sonido
        self.sonido_pellet = pygame.mixer.Sound("multimedia/wakawakalargo.wav")
        self.sonido_comerfantasma = pygame.mixer.Sound("multimedia/sonidocomerfantasma.wav")
        self.sonido_colisionfantasma = pygame.mixer.Sound("multimedia/muerte.wav")
        self.comiendo = False
        self.tiempo_ultimo_pellet = 0
        self.tiempo_maximo_entre_pellets = 0.25  # 250ms entre pellets para considerar que sigue comiendo

        self.sonido_muerte_reproducido = False



    def cargar_animaciones(self):
        # Diccionario para almacenar las animaciones por dirección
        self.skins = {
            ARRIBA: [],
            ABAJO: [],
            IZQUIERDA: [],
            DERECHA: []
        }

        # Cargar las imágenes para cada dirección
        for i in range(1, 7):  # Del 1 al 6 según los archivos de imágenes
            arr = pygame.image.load(f"multimedia/{i}_Arr.png").convert_alpha()
            self.skins[ARRIBA].append(arr)

            aba = pygame.image.load(f"multimedia/{i}_Aba.png").convert_alpha()
            self.skins[ABAJO].append(aba)

            der = pygame.image.load(f"multimedia/{i}_Der.png").convert_alpha()
            self.skins[DERECHA].append(der)

            izq = pygame.image.load(f"multimedia/{i}_Izq.png").convert_alpha()
            self.skins[IZQUIERDA].append(izq)

    def set_posicion_entre_nodos(self, nodo_origen, nodo_destino, porcentaje):
        """
        Establece la posición del Pacman entre dos nodos.
        nodo_origen: nodo desde donde viene
        nodo_destino: nodo hacia donde va
        porcentaje: valor entre 0.0 y 1.0 que indica qué tan lejos está del nodo_origen
        """
        self.nodo = nodo_origen
        self.blanco = nodo_destino
        self.porcentaje_entre_nodos = porcentaje
        # Calcular la posición exacta
        vec_direccion = self.blanco.posicion - self.nodo.posicion
        self.posicion = self.nodo.posicion + vec_direccion * porcentaje

        # Determinar la dirección basada en los nodos
        for direccion, vector in self.direcciones.items():
            if direccion != STOP:
                if self.nodo.vecinos[direccion] == self.blanco:
                    self.direccion = direccion
                    break



    def sonido_comer_pellet(self):
        """Inicia o mantiene el sonido de comer."""
        if not self.comiendo:
            self.sonido_pellet.play(-1)  # -1 significa reproducción en loop
            self.comiendo = True
        self.tiempo_ultimo_pellet = 0  # Resetear el contador

    def actualizar_sonido(self, dt):
        """Actualiza el estado del sonido basado en si Pacman sigue comiendo."""
        if self.comiendo:
            self.tiempo_ultimo_pellet += dt
            if self.tiempo_ultimo_pellet > self.tiempo_maximo_entre_pellets:
                self.sonido_pellet.stop()
                self.comiendo = False

    def morir(self):
        """Maneja la muerte de Pacman"""
        if not self.muerto:
            self.muerto = True
            self.tiempo_muerte = self.duracion_muerte
            self.vidas -= 1
            self.direccion = STOP
            self.visible = False  # Hace invisible a Pacman durante la muerte
            if self.comiendo:
                self.sonido_pellet.stop()
                self.comiendo = False

            if not self.sonido_muerte_reproducido:
                pygame.mixer.stop()
                self.sonido_colisionfantasma.play()
                self.sonido_muerte_reproducido = True

    def reset_posicion(self):
        """Resetea la posición de Pacman al punto inicial"""
        self.set_nodo_inicio(self.nodo_inicial)
        self.direccion = STOP
        self.direccion_deseada = STOP
        self.visible = True
        self.muerto = False
        self.sonido_muerte_reproducido = False

    def reset_vidas(self):
        self.reset_posicion()
        self.vidas=3

    def colision_fruta(self, fruta):
        """Verifica colisiones con la fruta."""
        if fruta and fruta.visible:
            distancia = self.posicion - fruta.posicion
            distancia_cuadrada = distancia.magnitudCuadrada()
            radio_total = (self.radio_colision + fruta.radio_colision) ** 2

            if distancia_cuadrada <= radio_total:
                return True
        return False

    def colision_con_fantasmas(self, fantasmas, grafo, textos_temporales):
        """
        Verifica colisiones con los fantasmas.
        Retorna los puntos si come un fantasma asustado,
        0 si no hay colisión o si Pacman muere.
        """
        # Itera sobre cada fantasma en el juego
        for fantasma in fantasmas:
            # Solo verifica colisiones si el fantasma está visible
            if fantasma.visible:
                # Colision circle to circle
                # Calcula la distancia entre Pacman y el fantasma
                distancia = self.posicion - fantasma.posicion
                # Calcula el cuadrado de la distancia (más eficiente que usar raíz cuadrada)
                distancia_cuadrada = distancia.magnitudCuadrada()
                # Calcula el radio total de colisión al cuadrado
                radio_total = (self.radio_colision + fantasma.radio_colision) ** 2

                # Verifica si hay colisión comparando las distancias
                if distancia_cuadrada <= radio_total:
                    # Si el fantasma está en modo FREIGHT (asustado/vulnerable)
                    if fantasma.modo.current == FREIGHT:
                        # Permite que el fantasma regrese a su casa
                        grafo.dar_acceso_a_casa(fantasma)
                        # Inicia el proceso de regeneración del fantasma
                        fantasma.iniciar_spawn()

                        # Reproduce el sonido de comer fantasma
                        self.sonido_comerfantasma.play()

                        # Obtiene los puntos por comer el fantasma
                        puntos = fantasma.puntos
                        # Actualiza los puntos para el siguiente fantasma (duplicándolos)
                        fantasmas.actualizar_puntos()

                        # Calcula la posición para mostrar el texto de puntos
                        pos_x = int(fantasma.posicion.x - 20)
                        pos_y = int(fantasma.posicion.y - 20)

                        # Crea un texto temporal que muestra los puntos ganados
                        texto = TextoTemporal(
                            texto=str(puntos),
                            posicion=(pos_x, pos_y),
                            duracion=1000,  # Duración en milisegundos
                            fuente=pygame.font.Font(None, 20),
                            color=(255, 255, 255)  # Color blanco
                        )
                        # Añade el texto temporal a la lista para ser mostrado
                        textos_temporales.append(texto)

                        return fantasma.puntos

                    # Si el fantasma no está en modo SPAWN y tampoco en FREIGHT
                    elif fantasma.modo.current != SPAWN:
                        # Pacman muere al tocar un fantasma normal
                        self.morir()
                        return 0
        # Si no hay colisiones, retorna 0 puntos
        return 0

    def animacion_muerte_terminada(self):
        """Verifica si la animación de muerte ha terminado"""
        return self.muerto and hasattr(self, 'animacion_muerte_completa') and self.animacion_muerte_completa

    def activar_poder(self):
        """Activa el poder y cambia el modo de los fantasmas."""
        self.tiene_poder = True
        self.tiempo_poder = self.duracion_poder
        for fantasma in self.fantasmas:
            fantasma.set_scatter_mode()

    def actualizar_poder(self, dt):
        """Actualiza el estado del poder."""
        if self.tiene_poder:
            self.tiempo_poder -= dt
            if self.tiempo_poder <= 0:
                self.tiene_poder = False
                self.tiempo_poder = 0
                for fantasma in self.fantasmas:
                    fantasma.modo = CHASE

    def comer_pellets(self, lista_pellets):
        """Verifica colisiones con pellets."""
        for pellet in lista_pellets:
            distancia = self.posicion - pellet.posicion
            distancia_potencia = distancia.magnitudCuadrada()
            radio_potencia = (pellet.radio + self.radio_colision) ** 2

            if distancia_potencia <= radio_potencia:
                # Activar o mantener el sonido de comer
                self.sonido_comer_pellet()

                if pellet.nombre == PELLETPODER:
                    self.activar_poder()
                return pellet
        return None

    def actualizar(self, dt):
        """Actualiza el estado de Pacman"""
        if self.muerto:
            if self.comiendo:
                self.sonido_pellet.stop()
                self.comiendo = False
            self.tiempo_muerte -= dt
            if self.tiempo_muerte <= 0:
                self.reset_posicion()
                self.animacion_muerte_completa = True
                return

        self.actualizar_animacion(dt)
        self.actualizar_poder(dt)
        self.actualizar_sonido(dt)

        if not self.muerto:
            direccion_nueva = self.entrada_teclado()

            # Permitir cambio de dirección incluso entre nodos si es dirección opuesta
            if self.direccion_opuesta(direccion_nueva):
                self.direccion_reversa()
                return

            # Actualizar posición actual
            self.posicion += self.direcciones[self.direccion] * self.velocidad * dt

            # Guardar la dirección deseada
            if direccion_nueva != STOP:
                self.direccion_deseada = direccion_nueva

            if self.blanco_sobrepasado():
                self.nodo = self.blanco

                if self.nodo.vecinos[PORTAL] is not None:
                    self.nodo = self.nodo.vecinos[PORTAL]

                # Intentar cambiar a la dirección deseada
                if self.direccion_deseada != STOP:
                    if self.validar_direccion(self.direccion_deseada):
                        self.direccion = self.direccion_deseada
                        self.direccion_deseada = STOP

                self.blanco = self.get_nuevo_blanco(self.direccion)

                if self.blanco is self.nodo:
                    self.direccion = STOP

                self.set_posicion()

    def render(self, pantalla):
        """Renderiza a Pacman en la pantalla"""
        if self.visible:
            if self.skin:
                # Obtener la posición como tupla de enteros
                p = self.posicion.entero()
                # Obtener el rectángulo de la imagen centrado en la posición actual
                rect = self.skin.get_rect(center=p)
                # Dibujar la imagen actual de la animación
                pantalla.blit(self.skin, rect)

    def entrada_teclado(self):
        teclaPresionada = pygame.key.get_pressed()
        if teclaPresionada[K_UP]:
            return ARRIBA
        if teclaPresionada[K_DOWN]:
            return ABAJO
        if teclaPresionada[K_LEFT]:
            return IZQUIERDA
        if teclaPresionada[K_RIGHT]:
            return DERECHA
        return STOP