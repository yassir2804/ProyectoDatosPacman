
# 🎮 Pac-Man Game

Un juego clásico de Pac-Man desarrollado en Python usando Pygame, con características modernas como sistema de guardado, múltiples niveles y efectos de sonido.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Cómo Jugar](#-cómo-jugar)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Controles](#-controles)
- [Sistema de Puntuación](#-sistema-de-puntuación)
- [Niveles](#-niveles)
- [Autores](#-autores)

## ✨ Características

### 🎯 Jugabilidad Principal
- **Pac-Man clásico**: Navega por el laberinto comiendo pellets y evitando fantasmas
- **4 fantasmas únicos**: Cada uno con su propia inteligencia artificial y comportamiento
- **Power Pellets**: Come pellets especiales para volver a los fantasmas vulnerables
- **Sistema de vidas**: Comienza con 3 vidas
- **Frutas especiales**: Aparecen periódicamente para puntos extra

### 🎨 Sistema Visual
- **Animaciones fluidas**: Sprites animados para Pac-Man y fantasmas
- **Efectos visuales**: Parpadeo del laberinto en modo power, transiciones de nivel
- **Múltiples niveles visuales**: Colores del laberinto cambian con cada nivel
- **Interfaz completa**: Contador de puntos, vidas, nivel actual

### 🎵 Audio
- **Efectos de sonido**: Sonidos para comer pellets, fantasmas, muerte, etc.
- **Música de fondo**: Música temática en el menú principal
- **Audio dinámico**: Los sonidos cambian según el estado del juego

### 💾 Funciones Avanzadas
- **Sistema de guardado**: Guarda y carga partidas completas
- **Menú principal**: Interfaz gráfica para iniciar o cargar juegos
- **Menú de pausa**: Pausa el juego y accede a opciones
- **Múltiples niveles**: Progresión a través de 3 niveles con dificultad creciente

## 📋 Requisitos

### Software Necesario
- Python 3.7 o superior
- Pygame 2.0 o superior
- NumPy

### Archivos Requeridos
El juego necesita los siguientes archivos en sus respectivas carpetas:
```
multimedia/
├── sprites de Pac-Man (1_Arr.png, 1_Der.png, etc.)
├── sprites de fantasmas (BlinkyArr.png, PinkyDer.png, etc.)
├── sprites de frutas (comodin_fres.png, comodin_vai.png, etc.)
├── efectos de sonido (.wav)
└── imagen de fondo (fototigrepacman.png)

Fuentes/
└── PressStart2P-Regular.ttf
```

## 🚀 Instalación

1. **Clona el repositorio**:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd ProyectoDatosPacman
   ```

2. **Instala las dependencias**:
   ```bash
   pip install pygame numpy
   ```

3. **Ejecuta el juego**:
   ```bash
   python Ejecutable.py
   ```

## 🎮 Cómo Jugar

### Objetivo
Come todos los pellets del laberinto mientras evitas a los fantasmas. Completa los 3 niveles para ganar el juego.

### Mecánicas Básicas
- **Pellets normales**: 10 puntos cada uno
- **Power Pellets**: 50 puntos + vuelve vulnerables a los fantasmas por 7 segundos
- **Fantasmas vulnerables**: 200, 400, 800, 1600 puntos (se duplican)
- **Frutas**: 100-500 puntos según el tipo

### Fantasmas
- **Blinky (Rojo)**: Persigue directamente a Pac-Man
- **Pinky (Rosa)**: Intenta emboscar a Pac-Man moviéndose hacia donde va
- **Inky (Azul)**: Comportamiento impredecible basado en Blinky
- **Clyde (Naranja)**: Alterna entre perseguir y huir

## 🎯 Controles

| Acción | Tecla |
|--------|-------|
| Mover Arriba | ↑ |
| Mover Abajo | ↓ |
| Mover Izquierda | ← |
| Mover Derecha | → |
| Pausa | ESC |
| Confirmar | ENTER |
| Navegar menús | ↑/↓ |

### Controles del Menú de Pausa
- **Reanudar**: Continúa el juego
- **Guardar Partida**: Guarda el progreso actual
- **Salir**: Cierra el juego

## 📊 Sistema de Puntuación

### Elementos Base
- **Pellet normal**: 10 puntos
- **Power Pellet**: 50 puntos
- **Fantasma (1º)**: 200 puntos
- **Fantasma (2º)**: 400 puntos
- **Fantasma (3º)**: 800 puntos
- **Fantasma (4º)**: 1600 puntos

### Frutas por Nivel
- **Nivel 1**: Fresa (100 puntos)
- **Nivel 2**: Uva (200 puntos)
- **Nivel 3**: Chocolate (300 puntos)
- **Especial**: Pacha (500 puntos) - 20% probabilidad

## 🎯 Niveles

### Progresión de Dificultad
- **Nivel 1**: Velocidad base de fantasmas
- **Nivel 2**: Fantasmas 20% más rápidos + laberinto rojo
- **Nivel 3**: Fantasmas 44% más rápidos + laberinto amarillo

### Mecánicas por Nivel
- Los fantasmas se liberan gradualmente (30 y 70 pellets comidos)
- Las frutas aparecen en momentos específicos (50 y 140 pellets)
- Colores del laberinto cambian para indicar progreso

## 📁 Estructura del Proyecto

```
ProyectoDatosPacman/
├── Ejecutable.py           # Punto de entrada principal
├── Controladora.py         # Lógica principal del juego
├── MenuPrincipal.py        # Menú de inicio
├── Pacman.py              # Clase del jugador
├── Fantasmas.py           # Clases de los fantasmas
├── Grafo.py               # Sistema de navegación del laberinto
├── Pellet.py              # Sistema de pellets
├── Fruta.py               # Sistema de frutas bonus
├── MapaVisual.py          # Renderizado del laberinto
├── Texto.py               # Sistema de UI y textos
├── Vector.py              # Matemáticas de vectores
├── Constantes.py          # Configuraciones globales
├── LevelManager.py        # Gestión de niveles
├── Modo.py                # Estados de los fantasmas
├── Entidad.py             # Clase base para elementos móviles
├── TextoTemporal.py       # Textos temporales (puntos)
├── MenuGameOver.py        # Pantalla de fin de juego
├── mazetest.txt           # Layout del laberinto
└── pacman_save.json       # Archivo de guardado (generado)
```

### Carpetas de Assets
```
multimedia/               # Imágenes y sonidos
Fuentes/                 # Archivos de fuentes
```

## 🔧 Características Técnicas

### Algoritmos Implementados
- **Pathfinding A***: Los fantasmas usan A* para navegación óptima
- **Sistema de caché**: Optimización de rutas calculadas
- **Detección de colisiones**: Círculo a círculo para precisión
- **Máquina de estados**: Gestión de modos de fantasmas

### Persistencia
- **Formato JSON**: Guardado completo del estado del juego
- **Datos guardados**: Posiciones, estados, puntuación, nivel, pellets restantes

## 👥 Autores

Desarrollado por:
- Saul
- Yassir
- Manuel
- Angel

## 📝 Notas de Desarrollo

### Archivos Importantes
- **mazetest.txt**: Define la estructura del laberinto
- **pacman_save.json**: Archivo de guardado automático
- **Constantes.py**: Configuraciones modificables del juego

### Personalización
Puedes modificar fácilmente:
- Velocidades en `Constantes.py`
- Colores del laberinto en `MapaVisual.py`
- Puntuaciones en `Pellet.py` y `Fruta.py`
- Comportamiento de fantasmas en `Fantasmas.py`

### Resolución de Problemas
- **Archivos faltantes**: Asegúrate de tener todos los assets en `multimedia/`
- **Errores de sonido**: Verifica que los archivos `.wav` estén presentes
- **Problemas de guardado**: El juego creará `pacman_save.json` automáticamente

---

¡Disfruta jugando! 🎮👾
