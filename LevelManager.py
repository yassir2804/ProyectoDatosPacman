class LevelManager:
    """
    Clase que gestiona los niveles del juego Pac-Man.
    Controla la progresión de niveles y ajusta la dificultad mediante
    la velocidad de los fantasmas.
    """

    def __init__(self):
        """
        Inicializa el gestor de niveles con valores predeterminados.
        """
        # Nivel actual del juego (comienza en 1)
        self.nivel_actual = 1

        # Velocidad base de los fantasmas en píxeles por segundo
        self.velocidad_base_fantasmas = 100

        # Factor de multiplicación de velocidad entre niveles
        # Cada nivel incrementa la velocidad en un 20%
        self.factor_velocidad = 1.2

    def subir_nivel(self):
        """
        Intenta avanzar al siguiente nivel.
        """
        if self.nivel_actual >= 3:  # Límite máximo de 3 niveles
            return False

        self.nivel_actual += 1
        return True

    def obtener_velocidad_fantasmas(self):
        """
        Calcula la velocidad actual de los fantasmas basada en el nivel.
        La velocidad aumenta exponencialmente con cada nivel.
        """
        return self.velocidad_base_fantasmas * (self.factor_velocidad ** (self.nivel_actual - 1))

    def verificar_nivel_completado(self, Pellet):
        """
        Verifica si se han comido todos los pellets del nivel actual.
        """
        return len(Pellet.listaPellets) == 0