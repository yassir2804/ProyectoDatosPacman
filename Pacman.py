import  pygame
import sys
import os

# Inicializa Pygame
pygame.init()
pygame.mixer.init()

eat_sound = pygame.mixer.Sound(os.path.join('multimedia', 'musica_pacman_chomp.wav'))

# Configuración de la pantalla
CELL_SIZE = 20
MAP_WIDTH = 28
MAP_HEIGHT = 31
SCORE_HEIGHT = 40  # Height for the score area
screen_width = CELL_SIZE * MAP_WIDTH
screen_height = (CELL_SIZE * MAP_HEIGHT) + SCORE_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pacman Clásico")

# Colores
COLOR_PARED = (0, 0, 150)
COLOR_FONDO = (0, 0, 0)
COLOR_PUNTO = (255, 255, 255)
COLOR_POWER_PELLET = (255, 182, 193)

# Cargar y redimensionar imágenes de Pacman
cantidadImagenes = 6
imagenes = [[] for _ in range(4)]

def cargar_y_redimensionar(ruta):
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, (CELL_SIZE, CELL_SIZE))

for i in range(1, cantidadImagenes + 1):
    imagenes[0].append(cargar_y_redimensionar(os.path.join('multimedia', f'{i}_Izq.png')))
    imagenes[1].append(cargar_y_redimensionar(os.path.join('multimedia', f'{i}_Der.png')))
    imagenes[2].append(cargar_y_redimensionar(os.path.join('multimedia', f'{i}_Arr.png')))
    imagenes[3].append(cargar_y_redimensionar(os.path.join('multimedia', f'{i}_Aba.png')))

# Definición del mapa
mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1],
    [1, 1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1],
    [1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1],
    [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1],
    [1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1],
    [1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1],
    [1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1],
    [1, 1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1, 1],
    [1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1],
    [1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
    [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
    [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Funciones del juego
def dibujar_pared_redondeada(superficie, rect):
    pygame.draw.rect(superficie, COLOR_PARED, rect, border_radius=3)

def crear_mapa_extendido(mapa_original):
    mapa_extendido = []
    for fila in mapa_original:
        nueva_fila = [fila[-1]] + fila + [fila[0]]
        mapa_extendido.append(nueva_fila)
    return mapa_extendido

# Extender el mapa
mapa = crear_mapa_extendido(mapa)

# Actualizar dimensiones
MAP_WIDTH = len(mapa[0])
screen_width = CELL_SIZE * (MAP_WIDTH - 2)  # Restamos 2 para excluir las columnas invisibles
screen = pygame.display.set_mode((screen_width, screen_height))

# Funciones del juego actualizadas
def dibujar_mapa(mapa):
    for y, fila in enumerate(mapa):
        for x in range(1, len(fila) - 1):  # Excluye la primera y última columna
            celda = fila[x]
            rect = pygame.Rect((x - 1) * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if celda == 1:  # Pared
                dibujar_pared_redondeada(screen, rect)
            elif celda == 2:  # Punto
                pygame.draw.circle(screen, COLOR_PUNTO, rect.center, CELL_SIZE // 8)
            elif celda == 3:  # Power Pellet
                pygame.draw.circle(screen, COLOR_POWER_PELLET, rect.center, CELL_SIZE // 3)

def puede_moverse(row, col, mapa):
    col = col % len(mapa[0])  # Asegura que la columna esté dentro del rango
    if 0 <= row < len(mapa):
        return mapa[row][col] != 1
    return False

# Variables del juego (ajustadas si es necesario)

pacman_col, pacman_row = 14, 23  # Ajustar si es necesario debido al mapa extendido
pacman_x, pacman_y = pacman_col * CELL_SIZE, pacman_row * CELL_SIZE
direction = 1  # Derecha inicialmente
next_direction = 1
vidas = 3
puntuacion = 0
frame_count = 0
paused = False


def comer_punto(row, col, mapa, puntuacion):
    if mapa[row][col] == 2:  # Punto normal
        mapa[row][col] = 0
        return puntuacion + 10
    elif mapa[row][col] == 3:  # Power Pellet
        mapa[row][col] = 0
        return puntuacion + 50
    return puntuacion

def dibujar_vidas(screen, vidas):
    for i in range(vidas):
        screen.blit(imagenes[1][0], (screen_width - (i + 1) * 30, screen_height - 30))

def perder_vida():
    global vidas, pacman_row, pacman_col, pacman_x, pacman_y
    vidas -= 1
    if vidas > 0:
        pacman_row, pacman_col = 23, 13
        pacman_x, pacman_y = pacman_col * CELL_SIZE, pacman_row * CELL_SIZE
    else:
        print("Game Over")
        pygame.quit()
        sys.exit()

def animar_pacman(direction, frame_count):
    animation_speed = 4
    frame_index = (frame_count // animation_speed) % len(imagenes[direction])
    return imagenes[direction][frame_index]

# Variables del juego
pacman_col, pacman_row = 13, 23
pacman_x, pacman_y = pacman_col * CELL_SIZE, pacman_row * CELL_SIZE
direction = 1  # Derecha inicialmente
next_direction = 1
vidas = 3
puntuacion = 0
frame_count = 0
paused = False

direcciones = {
    0: (0, -1),  # Izquierda
    1: (0, 1),   # Derecha
    2: (-1, 0),  # Arriba
    3: (1, 0)    # Abajo
}

VELOCIDAD = 2

clock = pygame.time.Clock()

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    if not paused:
        current_image = animar_pacman(direction, frame_count)
        screen.blit(current_image, (int(pacman_x) - CELL_SIZE, int(pacman_y)))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            next_direction = 0
        elif keys[pygame.K_RIGHT]:
            next_direction = 1
        elif keys[pygame.K_UP]:
            next_direction = 2
        elif keys[pygame.K_DOWN]:
            next_direction = 3

        center_x = pacman_x + CELL_SIZE // 2
        center_y = pacman_y + CELL_SIZE // 2

        if abs(center_x - (pacman_col + 0.5) * CELL_SIZE) < VELOCIDAD and \
           abs(center_y - (pacman_row + 0.5) * CELL_SIZE) < VELOCIDAD:
            dx, dy = direcciones[next_direction]
            new_row, new_col = int(pacman_row + dx), int(pacman_col + dy)

            if puede_moverse(new_row, new_col, mapa):
                direction = next_direction
                pacman_row, pacman_col = new_row, new_col
            else:
                dx, dy = direcciones[direction]
                new_row, new_col = int(pacman_row + dx), int(pacman_col + dy)
                if puede_moverse(new_row, new_col, mapa):
                    pacman_row, pacman_col = new_row, new_col

        target_x, target_y = pacman_col * CELL_SIZE, pacman_row * CELL_SIZE

        if pacman_col <= 0 and direction == 0:
            pacman_col = len(mapa[0]) - 2
            pacman_x = (len(mapa[0]) - 3) * CELL_SIZE
        elif pacman_col >= len(mapa[0]) - 1 and direction == 1:
            pacman_col = 1
            pacman_x = 0

        dx = target_x - pacman_x
        dy = target_y - pacman_y

        pacman_x += (VELOCIDAD if dx > 0 else -VELOCIDAD) if abs(dx) > VELOCIDAD else dx
        pacman_y += (VELOCIDAD if dy > 0 else -VELOCIDAD) if abs(dy) > VELOCIDAD else dy

        puntuacion = comer_punto(pacman_row, pacman_col, mapa, puntuacion)

        frame_count += 1

    screen.fill(COLOR_FONDO)

    # Dibujar el tablero de juego
    for y, fila in enumerate(mapa):
        for x, celda in enumerate(fila):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if celda == 1:  # Pared
                dibujar_pared_redondeada(screen, rect)
            elif celda == 2:  # Punto
                pygame.draw.circle(screen, COLOR_PUNTO, rect.center, CELL_SIZE // 8)
            elif celda == 3:  # Power Pellet
                pygame.draw.circle(screen, COLOR_POWER_PELLET, rect.center, CELL_SIZE // 3)

    if not paused:
        current_image = animar_pacman(direction, frame_count)
        screen.blit(current_image, (int(pacman_x), int(pacman_y)))
    else:
        font = pygame.font.Font(None, 74)
        texto_pausa = font.render("PAUSA", True, (255, 255, 255))
        screen.blit(texto_pausa, (screen_width // 2 - texto_pausa.get_width() // 2,
                                  (screen_height - SCORE_HEIGHT) // 2 - texto_pausa.get_height() // 2))

    # Dibujar línea separadora
    pygame.draw.line(screen, COLOR_PARED, (0, screen_height - SCORE_HEIGHT),
                     (screen_width, screen_height - SCORE_HEIGHT), 2)

    # Dibujar puntuación
    font = pygame.font.Font(None, 36)
    texto_puntuacion = font.render(f"Puntuación: {puntuacion}", True, (255, 255, 255))
    screen.blit(texto_puntuacion, (10, screen_height - SCORE_HEIGHT + 5))

    # Dibujar vidas
    dibujar_vidas(screen, vidas)

    pygame.display.flip()
    clock.tick(60)