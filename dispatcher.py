from gc import set_debug
from random import randint
from time import time as now
from constants import WHITE, RNG, MovementVector2D
from computed import alphaFromZ
from drone import DroneState
from render_util import drawAlphaCoordBlock

class DroneGenerator:
    def tick(self) -> bool:
        raise NotImplementedError("Drone Generator not implemented")

class PeriodicGenerator(DroneGenerator):
    def __init__(self, period: float, prob:float = 0.6, seed:int =randint(0, 10000)):
        self.period: float = period
        self.prob: float = prob
        self.seed: int = seed
        self.rng: RNG = RNG(seed)
        self.iter = 0
        self.last_iter = 0

    def tick(self) -> bool:
        if (self.iter - self.last_iter > self.period):
            self.last_iter = self.iter
            if (self.rng.randint(0, 100) < self.prob * 100):
                return True
        return False

    def update(self): 
        self.iter += 1


# potentially queue up multiple drones with different priorities and speeds etc
# generator just indicates if a drone has to be made, dispatch unit actually sets the drone up
# places drone at the correct starting point
class DispatchUnit:
    def __init__(self, x, y, dir, priority=0, generator: DroneGenerator = PeriodicGenerator(5), name="Dispatch Unit"):
        self.x = x
        self.y = y
        self.dir = dir
        self.priority = priority
        self.count = 0
        self.generator = generator
        self.name = name

    def dispatch(self):
        if self.generator.tick():
            self.count += 1
            return DroneState(MovementVector2D(self.x, self.y, self.dir), prioirty=self.priority, name=f"{self.name}-{self.count}")

    def render(self, zIdx):
        drawAlphaCoordBlock(self.x, self.y, (*WHITE, alphaFromZ(zIdx)), border=5)

    def update(self):
        self.generator.update()
        
#TODO: mark as vertiport (joby aviation, Bell Labs)

# marks drone as received/ goals are set to receive units/ will fire drone's graceful shutdown
# not a separate command in the map file format, will be created as new goals are created
class ReceiveUnit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ref_count = 0

    def __eq__(self, other):
        if type(other) == type(self):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def receive(self, drone: DroneState):
        drone.shutdown()
    
    def has(self, x, y):
        return x == self.x and y == self.y