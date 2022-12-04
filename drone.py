# forward declare types
from __future__ import annotations

from math import inf
from computed import alphaFromZ
from time import sleep
from render_util import drawAlphaCoordBlock, drawDroneIcon
from constants import *
from utils import uid

class DroneType:
    """
    Class to represent a type of drones. Will keep track of physical attributes of the drone.
    TODO: This will be useful with the AirCell class where the drone type will determine what weather the drone can fly through. 
    """
    def __init__(self):
        pass

class SmallDroneType(DroneType):
    """
    A small drone type, akin to ...
    TODO: Ask Saanvi
    """
    def __init__(self, max_wind_speed: float, min_wind_speed: float):
        pass

class DroneState:
    """
    DroneStates hold the state of a drone (speed, priority) for the simulation. 
    The program we write on the drone agent will not receive a DroneState, but a context of this state that will have copied values so a malicious program cannot modify the simulation
    """
    def __init__(self, movement_vector: MovementVector2D, name: str = "", prioirty: int = 0, goal: tuple[int, int] = None):
        self.id: str = uid()
        """
        A unique identifier representing the drone.
        """
        self.name: str = name
        """
        A name for the drone. This is not unique
        """
        self.priority: int = prioirty
        """
        The priority of the drone. Lower numbers mean higher priority.
        """
        self.movement_vector: MovementVector2D = movement_vector
        """
        Movement vector representing the current movement of the drone.
        """
        self.inital_vector: MovementVector2D = MovementVector2D(movement_vector.x, movement_vector.y, movement_vector.direction)
        """
        Movement vector representing the initial state of the drone.
        """
        self.goal: tuple[int, int] = goal
        """
        Coordinate representing the final destination of the Drone. When this is None, it will be assumed that the drone is trying to exit the Map Area.
        """
    
    def getCoords(self) -> Point2D:
        """
        Returns teh coordinates of the drone from its movement vector.
        """
        return self.movement_vector.getCoords() if self.movement_vector else None

    def getDirection(self) -> Action2D:
        """
        Returns the direction of the drone from its movement vector.
        """
        return self.movement_vector.direction if self.movement_vector else None
    
    def applyAction(self, action: Action2D):
        """
        Applies the given action to the drone, updating it's movement vector.
        """
        self.movement_vector = self.movement_vector.nextMovementVector(action)

    def render(self, zIdx: int):   
        """
        Renders the drone onto the screen.
        """
        drawDroneIcon(
            self.getCoords().x,
            self.getCoords().y,
            self.priority
        ) 
        # drawAlphaCoordBlock(
        #     self.getCoords().x,
        #     self.getCoords().y,
        #     (*priorityColorMap[self.priority], alphaFromZ(zIdx))
        # )
    
    def shutdown(self):
        """
        Gracefully shuts down the drone.
        """
        print("[SIM]", "Drone " + self.name + "[" + self.id + "]" + " shut down gracefully.")

class MemoryContext(dict):
    """
    A class to hold the memory of a drone. Basically a dictionary for the time being. Store data in a key-value fashion.
    """
    def __getattr__(self, __name: str) -> any:
        return self[__name]
    def __setattr__(self, __name: str, __value: any):
        self[__name] = __value
    

class DroneStateContext:
    """
    A class to pass a drone state from the simulation into the program. 
    This class exists to prevent a user from directly interacting with the simulation.
    Contains a copy of the simulation DroneState with only those attributes and behaviours that are required by the User program.
    """
    def __init__(self, state: DroneState, mem: MemoryContext):
        self.id: str = state.id
        """
        A unique identifier representing the drone.
        """
        self.name: str = state.name
        """
        A name for the drone. This is not unique
        """
        self.priority: int = state.priority
        """
        The priority of the drone. Lower numbers mean higher priority.
        """
        self.x: int = state.movement_vector.getCoords().x
        """
        Current x coordinate of the drone.
        """
        self.y: int = state.movement_vector.getCoords().y
        """
        Current y coordinate of the drone.
        """
        self.dir: Action2D = state.movement_vector.direction
        """
        Current direction of the drone.
        """
        self.init_x: int = state.inital_vector.getCoords().x
        """
        Initial x coordinate of the drone
        """
        self.init_y: int = state.inital_vector.getCoords().y
        """
        Initial y coordinate of the drone
        """
        self.init_dir: Action2D = state.inital_vector.direction
        """
        Initial direction of the drone
        """
        self.goal_x: int = state.goal.x if state.goal else inf
        """
        x coordinate of Goal of the drone
        """
        self.goal_y: int = state.goal.y if state.goal else inf
        """
        y coordinate of Goal of the drone
        """
        self.mem: MemoryContext = mem
        """
        The memory context belonging to this drone.
        """