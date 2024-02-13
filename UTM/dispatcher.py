# forward declare types
from __future__ import annotations

from random import randint
from UTM.constants import WHITE, RNG, MovementVector2D
from UTM.computed import alphaFromZ
from UTM.drone import DroneState
from UTM.render_util import drawAlphaCoordBlock

class BinaryProbabilityDistribution:
    """
    A BinaryProbabilityDistribution is a class that will help generate a sequenece of boolean values of true and false.
    """
    def tick(self) -> bool:
        """
        Abstract:
        Every time this function is called, the generator will generate a new boolean value.
        """
        raise NotImplementedError("Drone Generator not implemented")

class BinaryPeriodicDistribution(BinaryProbabilityDistribution):
    """
    A BinaryPeriodicDistribution will generate a single true over a period given a probability value.
    A seed can optionally be provieded to control the sequence generated. 
    """
    def __init__(self, period: float, prob:float = 0.8, seed:int =randint(0, 10000)):
        self.period: float = period
        """
        The interval length for one true value.
        """
        self.prob: float = prob
        """
        The probability with which the true will be generated over that period.
        """
        self.seed: int = seed
        """
        The seed that this generator is based on.
        """
        self.rng: RNG = RNG(seed)
        """
        The random number generator to generate a sequence of random numbers that will be converted to a boolean distribution.
        """
        self.iter: int = 0
        """
        Number of iterations that have passed (to keep track of the period).
        """
        self.last_iter: int = 0
        """
        Number of iterations that have passed since last generation (to keep track of the period).
        """

    def tick(self) -> bool:
        """
        If the difference in the iter and last_iter is greater than or equal to the period, it will attempt to generate a True with the given probability.
        """
        if (self.iter - self.last_iter >= self.period):
            self.last_iter = self.iter
            return self.rng.randint(0, 100) < self.prob * 100
        return False

    def update(self): 
        """
        Called to keep track of the number of iterations that have passed in the simulation to keep track of the period.
        """
        self.iter += 1


# potentially queue up multiple drones with different priorities and speeds etc
# generator just indicates if a drone has to be made, dispatch unit actually sets the drone up
# places drone at the correct starting point
class DispatchVertiport:
    """
    Currently Dispatch Vertiports serve to provide a form of traffic generation.
    Given a coordinate, a priority and a direction, dispatch vertiports generate drones with those attributes.
    
    Dispatch Units are powered by DroneGenerators, that can have different probabilistic distributions powering them.
    The main working is, the unit will tick the generator every iteration, and if the tick returns true it will dispatch a drone on the map.

    TODO: add drone destination properties.
    TODO: look into -> joby aviation, Bell Labs
    """
    def __init__(self, x: int, y: int, dir: "Direction2D", priority: int = 0, generator: BinaryProbabilityDistribution = BinaryPeriodicDistribution(5), name: str ="Dispatch Unit"):
        self.x: int = x
        """
        x coordinate of the vertiport on the map.
        """
        self.y: int = y
        """
        y coordinate of the vertiport on the map.
        """
        self.dir: "Direction2D" = dir
        """
        direction that the drones are spawned in.
        """
        self.priority: int = priority
        """
        priority of the drones spawned in.
        """
        self.count: int = 0
        """
        keeps track of how many drones are spawned by this vertiport.
        """
        self.generator: BinaryProbabilityDistribution = generator
        """
        A DroneGenerator that has a probabilistic model to allow this dispatch unit to spawn drones.
        """
        self.name: str = name
        """
        Name of this dispatch unit.
        """

    def dispatch(self) -> DroneState:
        if self.generator.tick():
            self.count += 1
            return DroneState(MovementVector2D(self.x, self.y, self.dir), prioirty=self.priority, name=f"{self.name}-{self.count}")

    def render(self, zIdx: int):
        drawAlphaCoordBlock(self.x, self.y, (*WHITE, alphaFromZ(zIdx)), border=5)

    def update(self):
        self.generator.update()
        
# marks drone as received/ goals are set to receive units/ will fire drone's graceful shutdown
# not a separate command in the map file format, will be created as new goals are created
class ReceiveVertiport:
    """
    Receive vertiports are the opposite of dispatch vertiports, they will receive drones if the drone goal matches the receive vertiport.
    The drone goal can currently only be a receive vertiport's coordinates, or it can be out of bounds for the map to pick up once the drone goes offscreent.
    """
    def __init__(self, x: int, y: int):
        self.x: int = x
        """
        The x coordinate of the receive vertiport.
        """
        self.y: int = y
        """
        The y coordinate of the receive vertiport.
        """
        self.ref_count: int = 0
        """
        The number of drones this vertiport has received.
        """

    def __eq__(self, other: ReceiveVertiport):
        """
        Compares two receive vertiports on the basis that their coordinates are equal.
        """
        if type(other) == type(self):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self) -> int:
        """
        Hashes the vertiports to ensure that 2 vertiports that are equal will have the same hash.
        """
        return hash((self.x, self.y))

    def receive(self, drone: DroneState):
        """
        Will gracefully shutdown the drone and then update its reference count, given that this vertiport was the drone's goal.
        """
        drone.shutdown()
        self.ref_count += 1
    
    def has(self, x: int, y: int) -> bool:
        """
        Will check if the vertiport is at the given x and y coordinate.
        """
        return x == self.x and y == self.y