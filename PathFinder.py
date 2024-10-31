from heapq import heappush, heappop
from Vector import Vector1

class PathFinder:
    def __init__(self, grafo):
        self.grafo = grafo
        # Updated to use numeric constants for directions
        self.prioridad_direcciones = {
            1: 0,    # ARRIBA
            2: 1,    # IZQUIERDA
            -1: 2,   # ABAJO
            -2: 3,   # DERECHA
            0: 4     # STOP
        }

    def heuristica(self, nodo_pos, objetivo_pos):
        """Calcula la distancia Manhattan entre dos posiciones"""
        return abs(nodo_pos.x - objetivo_pos.x) + abs(nodo_pos.y - objetivo_pos.y)

    def obtener_camino(self, actual, came_from):
        """Reconstruye el camino desde el nodo final hasta el inicio"""
        camino = []
        while actual in came_from:
            camino.append(actual)
            actual = came_from[actual]
        camino.append(actual)
        return list(reversed(camino))

    def encontrar_ruta(self, inicio, objetivo, direccion_actual=None):
        """
        Implementa A* para encontrar la mejor ruta entre dos nodos, usando prioridades para desempatar
        """
        if inicio is None or objetivo is None:
            return None

        visitados = set()
        cola = []
        came_from = {}
        g_score = {inicio: 0}
        f_score = {inicio: self.heuristica(inicio.posicion, objetivo.posicion)}

        heappush(cola, (f_score[inicio], 0, id(inicio), inicio))

        # Actualizado para usar direcciones numéricas
        direcciones_opuestas = {
            1: -1,    # ARRIBA : ABAJO
            -1: 1,    # ABAJO : ARRIBA
            2: -2,    # IZQUIERDA : DERECHA
            -2: 2,    # DERECHA : IZQUIERDA
            0: 0      # STOP : STOP
        }

        while cola:
            _, _, _, actual = heappop(cola)

            if actual == objetivo:
                camino = self.obtener_camino(actual, came_from)
                if len(camino) >= 2:
                    direcciones_validas = []
                    for direccion, vecino in camino[0].vecinos.items():
                        if vecino == camino[1]:
                            if direccion in self.prioridad_direcciones:  # Validación añadida
                                if direccion_actual is None or direcciones_opuestas.get(direccion) != direccion_actual:
                                    direcciones_validas.append((self.prioridad_direcciones[direccion], direccion))

                    if direcciones_validas:
                        return min(direcciones_validas, key=lambda x: x[0])[1]

                    # Si todas son giros de 180°
                    direcciones_180 = []
                    for direccion, vecino in camino[0].vecinos.items():
                        if vecino == camino[1] and direccion in self.prioridad_direcciones:  # Validación añadida
                            direcciones_180.append((self.prioridad_direcciones[direccion], direccion))
                    return min(direcciones_180, key=lambda x: x[0])[1] if direcciones_180 else None
                return None

            visitados.add(actual)

            for direccion, vecino in actual.vecinos.items():
                if vecino is None or direccion == 5:  # 5 for PORTAL constant
                    continue

                if vecino in visitados:
                    continue

                if actual == inicio and direccion_actual is not None:
                    if direcciones_opuestas.get(direccion) == direccion_actual:
                        continue

                tentative_g = g_score[actual] + 1

                if vecino not in g_score or tentative_g < g_score[vecino]:
                    came_from[vecino] = actual
                    g_score[vecino] = tentative_g
                    f_nuevo = tentative_g + self.heuristica(vecino.posicion, objetivo.posicion)
                    f_score[vecino] = f_nuevo

                    if direccion in self.prioridad_direcciones:  # Validación añadida
                        if vecino not in [n for _, _, _, n in cola]:
                            heappush(cola, (f_nuevo, self.prioridad_direcciones[direccion], id(vecino), vecino))

        return None