
class fantasma:
    def __init__(self, nodo, pacman=None, blinky=None):
        Entity.__init__(self, nodo)
        self.nombre = GHOST
        self.puntos = 200
        self.objetivo = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.modo = ModoController(self)
        self.blinky = blinky
        self.NodoCasa = node

    def reset(self):
        Entity.reset(self)
        self.puntos= 200
        self.directionMethod = self.goalDirection

    def update(self, dt):
        self.sprites.update(dt)
        self.modo.update(dt)
        if self.modo .current is SCATTER:
            self.scatter()
        elif self.modo.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.objetivo = Vector2()

    def chase(self):
        self.objetivo = self.pacman.position

    def spawn(self):
        self.objetivo = self.NodoDeSpawn.position

    def setNodoDeSpawn(self, node):
        self.NodoDeSpawn = node

    def startSpawn(self):
        self.modo.setSpawnMode()
        if self.modo.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def startFreight(self):
        self.modo.setFreightMode()
        if self.modo.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection

    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirectio

class Blinky(fantasma):
    def __init__(self, nodo,pacman=None, blinky=None):
        fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre=Blinky
        self.color= Red

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.objetivo= Vector2()

    def chase(self):
        self.objetivo= 0




class Pinky(fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre = Blinky
        self.color = Pinky

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.objetivo = 0

    def chase(self):
        self.objetivo = 0


class Inky(fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre = Inky
        self.color = Teal

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.objetivo = 0

    def chase(self):
        self.objetivo = 0


class Clyde(fantasma):
    def __init__(self, nodo, pacman=None, blinky=None):
        fantasma.__init__(self, nodo, pacman, blinky)
        self.nombre = Clyde
        self.color = Orange

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.objetivo = 0

    def chase(self):
        self.objetivo = 0



class GrupoFantasma(Object):
    def __init__(self,nodo,pacman):
        self.blinky = Blinky(nodo,pacman)
        self.Pinky = Pinky(nodo,pacman)
        self.Inky = Inky(nodo,pacman)
        self.Clyde = Clyde(nodo,pacman)
        self.fantasmas = [self.blinky,self.Pinky,self.Inky,self.Clyde]

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)

    def startFreight(self):
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def reset(self):
        for ghost in self:
            ghost.reset()

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)
