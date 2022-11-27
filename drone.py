from math import inf
from computed import alphaFromZ
from time import sleep
from render_util import drawAlphaCoordBlock
from constants import *
from utils import uid

class DroneType:
    def __init__(self):
        pass

class SmallDroneType(DroneType):
    def __init__(self, max_wind_speed, min_wind_speed):
        pass

class DroneState:
    """
    DroneStates hold the state of a drone (speed, priority)
    """
    def __init__(self, movement_vector: MovementVector2D, name="", prioirty=0, goal = None):
        self.id = uid()
        self.name = name
        self.priority = prioirty
        self.movement_vector = movement_vector
        self.inital_vector = MovementVector2D(movement_vector.x, movement_vector.y, movement_vector.direction)
        self.goal = goal
    
    def getCoords(self):
        return self.movement_vector.getCoords() if self.movement_vector else None

    def getDirection(self):
        return self.movement_vector.direction if self.movement_vector else None
    
    def applyAction(self, action):
        self.movement_vector = self.movement_vector.nextMovementVector(action)

    def render(self, zIdx):    
        drawAlphaCoordBlock(
            self.getCoords().x,
            self.getCoords().y,
            (*priorityColorMap[self.priority], alphaFromZ(zIdx))
        )
    
    def shutdown(self):
        print("[SIM]", "Drone " + self.name + "[" + self.id + "]" + " shut down gracefully.")

class MemoryContext(dict):
    def __getattr__(self, __name: str):
        return self[__name]
    def __setattr__(self, __name: str, __value):
        self[__name] = __value
    

class DroneStateContext:
    def __init__(self, state: DroneState, mem: MemoryContext):
        self.id = state.id
        self.name = state.name
        self.priority = state.priority
        self.x = state.movement_vector.getCoords().x
        self.y = state.movement_vector.getCoords().y
        self.dir = state.movement_vector.direction
        self.init_x = state.inital_vector.getCoords().x
        self.init_y = state.inital_vector.getCoords().y
        self.init_dir = state.inital_vector.direction
        self.goal_x = state.goal.x if state.goal else inf
        self.goal_y = state.goal.y if state.goal else inf
        self.mem = mem