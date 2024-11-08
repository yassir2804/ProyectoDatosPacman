#Aqui se añadiran todas los valores que se reutilizaran  en distintas secciones del código para facilitar su acceso

#Configuraciones de pantalla
ALTURACELDA = 20;
ANCHOCELDA = 20;
FILAS = 36
COLUMNAS = 28
ALTURAPANTALLA = ALTURACELDA * FILAS
ANCHOPANTALLA = ANCHOCELDA * COLUMNAS
TAMANIOPANTALLA = (ANCHOPANTALLA,ALTURAPANTALLA)

#COLORES
NEGRO = (255,255,255)
NEGRO = (0,0,0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
ROSADO = (255,192,203)
AZUL = (0,0,255)
NARANJA = (255,91,1)
CELESTE = (135,206,235)
PURPURA = (128, 0, 128)

#Direcciones
STOP = 0
ARRIBA = 1
ABAJO = -1
IZQUIERDA = 2
DERECHA = -2
PORTAL = 5

#Pacman
PACMAN = 0
PELLET = 1
PELLETPODER = 2
FANTASMA=3

SCATTER = 0
CHASE = 1
FREIGHT = 2
SPAWN = 3

#Constantes mapa
PARED = 'X'
CAMINO = '.'
NODO = '+'

#Constantes texto
SCORETXT = 0
LEVELTXT = 1
READYTXT = 2
PAUSETXT = 3
GAMEOVERTXT = 4
LEVELUPTXT= 5


#Constantes Fantasmas
BLINKY=99
CLYDE=98
PINKY=97
INKY=96

FRUTA = 22

ESTADO_EN_CASA = "en_casa"
ESTADO_SUBIENDO = "subiendo"
ESTADO_MOVIENDO_SALIDA = "moviendose_salida"
ESTADO_FUERA = "fuera"

# Velocidades
VELOCIDAD_CASA = 50
VELOCIDAD_NORMAL = 100
VELOCIDAD_FREIGHT = 50
VELOCIDAD_SPAWN = 150

# Tiempos
TIEMPO_ENTRE_FANTASMAS = 5  # segundos
DURACION_FREIGHT = 7  # segundos
TIEMPO_PARPADEO = 0.2  # segundos
