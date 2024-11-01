import pygame

# Clase base para las entidades
class Entity:
    def __init__(self, imagen=None):
        self.imagen = imagen
        self.x = 0  # Coordenada X de la entidad
        self.y = 0  # Coordenada Y de la entidad

    def render(self, pantalla):
        if self.imagen is not None:
            pantalla.blit(self.imagen, (self.x, self.y))  # Dibujar la imagen de la entidad
        else:
            # Dibujar un círculo como respaldo
            pygame.draw.circle(pantalla, (255, 255, 0), (self.x, self.y), 10)  # Cambiar color y tamaño según sea necesario

# Clase para Pacman
class Pacman(Entity):
    def __init__(self):
        super().__init__()
        # Cargar imágenes
        self.imagen_izquierda = pygame.image.load('pacman_izquierda.png').convert_alpha()
        self.imagen_derecha = pygame.image.load('pacman_derecha.png').convert_alpha()
        self.imagen_arriba = pygame.image.load('pacman_arriba.png').convert_alpha()
        self.imagen_abajo = pygame.image.load('pacman_abajo.png').convert_alpha()
        self.direccion = 2  # Dirección inicial (DERECHA)

    def set_direction(self, direccion):
        self.direccion = direccion

    def get_image(self):
        if self.direccion == 2:  # IZQUIERDA
            return self.imagen_izquierda
        elif self.direccion == -2:  # DERECHA
            return self.imagen_derecha
        elif self.direccion == 1:  # ARRIBA
            return self.imagen_arriba
        elif self.direccion == -1:  # ABAJO
            return self.imagen_abajo
        return self.imagen_derecha  # Dirección predeterminada

# Clase para los fantasmas
class Ghost(Entity):
    def __init__(self, nombre_archivo):
        super().__init__()
        # Cargar imagen del fantasma
        self.imagen = pygame.image.load(nombre_archivo).convert_alpha()