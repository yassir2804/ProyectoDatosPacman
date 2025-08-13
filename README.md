
# 🎮 Pac-Man Game

A classic Pac-Man game developed in Python using Pygame, featuring modern characteristics like save system, multiple levels, and sound effects.

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [How to Play](#-how-to-play)
- [Project Structure](#-project-structure)
- [Controls](#-controls)
- [Scoring System](#-scoring-system)
- [Levels](#-levels)
- [Authors](#-authors)

## ✨ Features

### 🎯 Core Gameplay
- **Classic Pac-Man**: Navigate through the maze eating pellets while avoiding ghosts
- **4 unique ghosts**: Each with their own artificial intelligence and behavior
- **Power Pellets**: Eat special pellets to make ghosts vulnerable
- **Lives system**: Start with 3 lives
- **Special fruits**: Appear periodically for extra points

### 🎨 Visual System
- **Smooth animations**: Animated sprites for Pac-Man and ghosts
- **Visual effects**: Maze blinking in power mode, level transitions
- **Multiple visual levels**: Maze colors change with each level
- **Complete interface**: Score counter, lives, current level

### 🎵 Audio
- **Sound effects**: Sounds for eating pellets, ghosts, death, etc.
- **Background music**: Thematic music in the main menu
- **Dynamic audio**: Sounds change according to game state

### 💾 Advanced Features
- **Save system**: Save and load complete games
- **Main menu**: Graphical interface to start or load games
- **Pause menu**: Pause the game and access options
- **Multiple levels**: Progress through 3 levels with increasing difficulty

## 📋 Requirements

### Required Software
- Python 3.7 or higher
- Pygame 2.0 or higher
- NumPy

### Required Files
The game needs the following files in their respective folders:
```
multimedia/
├── Pac-Man sprites (1_Arr.png, 1_Der.png, etc.)
├── ghost sprites (BlinkyArr.png, PinkyDer.png, etc.)
├── fruit sprites (comodin_fres.png, comodin_vai.png, etc.)
├── sound effects (.wav)
└── background image (fototigrepacman.png)

Fuentes/
└── PressStart2P-Regular.ttf
```

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone [REPOSITORY_URL]
   cd ProyectoDatosPacman
   ```

2. **Install dependencies**:
   ```bash
   pip install pygame numpy
   ```

3. **Run the game**:
   ```bash
   python Ejecutable.py
   ```

## 🎮 How to Play

### Objective
Eat all the pellets in the maze while avoiding ghosts. Complete all 3 levels to win the game.

### Basic Mechanics
- **Normal pellets**: 10 points each
- **Power Pellets**: 50 points + makes ghosts vulnerable for 7 seconds
- **Vulnerable ghosts**: 200, 400, 800, 1600 points (doubling)
- **Fruits**: 100-500 points depending on type

### Ghosts
- **Blinky (Red)**: Directly chases Pac-Man
- **Pinky (Pink)**: Tries to ambush Pac-Man by moving toward where he's going
- **Inky (Blue)**: Unpredictable behavior based on Blinky
- **Clyde (Orange)**: Alternates between chasing and fleeing

## 🎯 Controls

| Action | Key |
|--------|-----|
| Move Up | ↑ |
| Move Down | ↓ |
| Move Left | ← |
| Move Right | → |
| Pause | ESC |
| Confirm | ENTER |
| Navigate menus | ↑/↓ |

### Pause Menu Controls
- **Resume**: Continue the game
- **Save Game**: Save current progress
- **Exit**: Close the game

## 📊 Scoring System

### Base Elements
- **Normal pellet**: 10 points
- **Power Pellet**: 50 points
- **Ghost (1st)**: 200 points
- **Ghost (2nd)**: 400 points
- **Ghost (3rd)**: 800 points
- **Ghost (4th)**: 1600 points

### Fruits by Level
- **Level 1**: Strawberry (100 points)
- **Level 2**: Grape (200 points)
- **Level 3**: Chocolate (300 points)
- **Special**: Pacha (500 points) - 20% probability

## 🎯 Levels

### Difficulty Progression
- **Level 1**: Base ghost speed
- **Level 2**: Ghosts 20% faster + red maze
- **Level 3**: Ghosts 44% faster + yellow maze

### Level Mechanics
- Ghosts are released gradually (30 and 70 pellets eaten)
- Fruits appear at specific moments (50 and 140 pellets)
- Maze colors change to indicate progress

## 📁 Project Structure

```
ProyectoDatosPacman/
├── Ejecutable.py           # Main entry point
├── Controladora.py         # Main game logic
├── MenuPrincipal.py        # Start menu
├── Pacman.py              # Player class
├── Fantasmas.py           # Ghost classes
├── Grafo.py               # Maze navigation system
├── Pellet.py              # Pellet system
├── Fruta.py               # Bonus fruit system
├── MapaVisual.py          # Maze rendering
├── Texto.py               # UI and text system
├── Vector.py              # Vector mathematics
├── Constantes.py          # Global configurations
├── LevelManager.py        # Level management
├── Modo.py                # Ghost states
├── Entidad.py             # Base class for moving elements
├── TextoTemporal.py       # Temporary texts (points)
├── MenuGameOver.py        # Game over screen
├── mazetest.txt           # Maze layout
└── pacman_save.json       # Save file (generated)
```

### Asset Folders
```
multimedia/               # Images and sounds
Fuentes/                 # Font files
```

## 🔧 Technical Features

### Implemented Algorithms
- **A* Pathfinding**: Ghosts use A* for optimal navigation
- **Cache system**: Optimization of calculated routes
- **Collision detection**: Circle to circle for precision
- **State machine**: Ghost mode management

### Persistence
- **JSON format**: Complete game state saving
- **Saved data**: Positions, states, score, level, remaining pellets

## 👥 Authors

Developed by:
- Saul
- Yassir
- Manuel
- Angel

## 📝 Development Notes

### Important Files
- **mazetest.txt**: Defines the maze structure
- **pacman_save.json**: Automatic save file
- **Constantes.py**: Modifiable game configurations

### Customization
You can easily modify:
- Speeds in `Constantes.py`
- Maze colors in `MapaVisual.py`
- Scores in `Pellet.py` and `Fruta.py`
- Ghost behavior in `Fantasmas.py`

### Troubleshooting
- **Missing files**: Make sure you have all assets in `multimedia/`
- **Sound errors**: Verify that `.wav` files are present
- **Save problems**: The game will create `pacman_save.json` automatically

---

Enjoy playing! 🎮👾
