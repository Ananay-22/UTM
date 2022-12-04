# forward declare types
from __future__ import annotations

from enum import Enum
import random
from utils import getBlockSize, has

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GRAY = (69, 69, 69)
RED = (235, 67, 91)
GREEN = (67, 235, 91)
BLUE = (100, 30, 245)
PURPLE = (120, 50, 145)
ORANGE = (200, 125, 0)
YELLOW = (200, 200, 0)

color_lookup = {
    "O": BLACK, 
    "@": GRAY,
    ">": RED,
    "<": GREEN,
    "^": BLUE,
    "v": PURPLE
}
"""
Dictionary mapping symbols to colors, useful for legacy textbased map.
"""
priorityColorMap = {
    0: YELLOW
}
"""
Dictionary that will return the color of a drone based on it's priority. Replaced by priorityImageMap.
"""

priorityImageMap = {
    0: "./res/drone_icon.png"
}
"""
Dictionary that will return the image of a drone based on it's priority.
"""
BLOCK_SIZE = 32
"""
Pixel size of 1 block
"""
MAX_ELEMENTS_IN_BLOCK = 100 
"""
if there are more than 100 elements in a block, the highest ones are not visible
generally, optimize the simulation to have not more than 4-5 elements a block
"""

WINDOW_WIDTH = WINDOW_HEIGHT = 20 * BLOCK_SIZE # TODO: need to make windowing dependent on the map being rendered
"""
Dimension of the window, defaults to 20 Blocks.
"""
class Dimension2D:
    """
    Represents 2 Dimensional measurements.
    """
    def __init__(self, width, height):
        self.width = width
        """
        Width Dimension.
        """
        self.height = height
        """
        Height Dimension.
        """

class Point2D:
    """
    Represents 2 Dimensional Coordinates.
    """
    def __init__(self, x, y):
        self.x = x
        """
        x coordinate.
        """
        self.y = y
        """
        y coordinate.
        """

class Orientation2D(Enum):
    """
    Represents 2 Dimensional Orientation. Only Supports Standard Orientations (Vertical and Horizontal)
    """
    HORIZONTAL="H"
    VERTICAL="V"

class RNG:
    """
    Random Number Generator (Pseudo).
    Uses built in random generator.
    Since that generator doesnt have a discrete class but does have a state, this class just stores the state of the rng.
    """
    def __init__(self, seed):
        """
        When a new instance is created with a seed, it saves the current state of random, sets random the a new generator with the seed, stores that new state in this class, and restors the current version.
        """
        self.seed = seed
        """
        seed of the rng
        """
        # store global state
        old_state = random.getstate()

        # create our state
        random.seed(self.seed)
        # store our state to return
        self.rng = random.getstate()
        """
        Stores the value of random.getstate() for this instance of the rng
        """
        #restor global state
        random.setstate(old_state)

    def randint(self, a, b):
        """
        Functionally identical to random.randint() but with the seed for this instance without affecting the global random generator.
        """
        # store global state
        old_state = random.getstate()
        # create our state
        random.setstate(self.rng)
        # store our state to return
        ret = random.randint(a, b)

        # update our state
        self.rng = random.getstate()
        #restor global state
        random.setstate(old_state)
        #return our state
        return ret

class Action2D(Enum):
    """
    Represents 2 Dimensional Actions. Semantically equal to 2 Dimensional Directions (there is no separate class).
    """
    NORTH="N"
    SOUTH="S"
    EAST="E"
    WEST="W"
    NOP="O"

    @staticmethod
    def to_vec(vec):
        """
        Converts an Action to a Vector that can be thought of as a normal direction vector.
        """
        __vector_map = {
            Action2D.NORTH: ( 0, -1),
            Action2D.SOUTH: ( 0,  1),
            Action2D.WEST : (-1,  0),
            Action2D.EAST : ( 1,  0),
            Action2D.NOP  : ( 0,  0)
        }
        return __vector_map[vec]

    _ignore_ = ["RIGHT", "LEFT", "REVERSE"]

    RIGHT = dict()
    LEFT = dict()
    REVERSE = dict()

Action2D.RIGHT = {
        Action2D.NORTH: Action2D.EAST,
        Action2D.EAST: Action2D.SOUTH,
        Action2D.SOUTH: Action2D.WEST,
        Action2D.WEST: Action2D.WEST,
        Action2D.NOP: Action2D.NOP
    }
"""
Returns the Direction that is equivalent to a RIGHT at the given direction.
"""

Action2D.LEFT = dict([(y, x) for x, y in Action2D.RIGHT.items()])
"""
Returns the Direction that is equivalent to a LEFT at the given direction.
"""

Action2D.REVERSE = {
        Action2D.NORTH: Action2D.SOUTH,
        Action2D.WEST: Action2D.EAST,
        Action2D.SOUTH: Action2D.NORTH,
        Action2D.EAST: Action2D.WEST,
        Action2D.NOP: Action2D.NOP
    }
"""
Returns the Direction that is equivalent to a REVERSE at the given direction.
"""


class MovementVector2D:
    """
    MovementVector2Ds will hold the position and the direction of the object 
    TODO: Drone direction is it's next action. we assume for now that changing directions is instantaneous
    """

    def __init__(self, x, y, direction: Action2D):
        self.x = x
        """
        x coordinate of the object.
        """
        self.y = y
        """
        y cooredinate of the object.
        """
        self.direction = direction
        """
        Direction of the object.
        """

    def getCoords(self):
        """
        Get a Point2D Object representing the coordinate of the object.
        """
        return Point2D(self.x, self.y)

    def nextMovementVector(self, direction: Action2D):
        """
        Sets the current Direction to the one provided, then updates the coordinates to move in that direction.
        Does not update in place, but returns a new MovementVector
        """
        dx, dy = Action2D.to_vec(direction)
        return MovementVector2D(self.x + dx, self.y + dy, direction)



class DroneSimContext:
    """
    Represents the Information that will be passed into the drone. Can be thought of its memory + its sensed data.
    """
    def __init__(self, drone, sim_state):
        self.corridors = sim_state.corridors
        """
        List of Corridors on the map.
        """
        self.intersections = sim_state.intersections
        """
        List of intersections on the map.
        """
        self.comms_buffer = sim_state.comms.fetch(drone.id)
        """
        Packets received by the drone
        """
        self.dispatch = lambda packet: sim_state.comms.dispatch(packet) #todo add typing
        """
        Callable that the drone can use to dispatch packets into the Communication Fabric.
        """ 

    # def has(self, x, y):
    #     """
    #     Check if a given coordinate falls 
    #     """
    #     return has(x,y, 0, 0, self.dimension.width, self.dimension.height)
        
    def get_containing_corridor(self, x, y):
        """
        Return the first corridor in the list that the x, y coordinates fall in.
        """
        for corridor in self.corridors:
            if corridor.has(x, y):
                return corridor

    def get_containing_intersection(self, x, y):
        """
        Return the first intersection in the list that the x, y coordinates fall in.
        """
        for intersection in self.intersections:
            if intersection.has(x, y):
                return intersection