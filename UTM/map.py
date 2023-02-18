# forward declare types
from __future__ import annotations

from itertools import combinations
from UTM.agents import Agent, DroneAgent, ForwardDroneAgent
from UTM.comms import CommunicationFabric

from UTM.constants import BLUE, GRAY, GREEN, PURPLE, RED, WHITE, Dimension2D, DroneSimContext, Orientation2D
from UTM.computed import alphaFromZ
from UTM.dispatcher import DispatchVertiport, ReceiveVertiport
from UTM.drone import Action2D, DroneState, DroneStateContext, MemoryContext

from UTM.render_util import drawAlphaCoordBlock, drawArrow, drawCoordBlock
from UTM.utils import has

class Channel2D:
    """
    Class representing an individual channel in a 2D map.
    A channel is a line of air cells.
    The channels currently are unidirectional.
    Multiple channels make an aircorridor.
    """
    def __init__(self, idx: int, dir: Action2D, orientation: Orientation2D):
        self.idx: int = idx
        """
        The index of the channel in the corridor.
        """
        self.dir: Action2D = dir
        """
        The direction of the channel. Determines which directions the drones can move.
        """
        self.orientation: Orientation2D = orientation
        """
        The orientation of the channel on the map. Vertical or Horizontal.
        """
    
    def getDirection(self) -> Action2D:
        """
        Returns the direction of the channel. Drones must flow along this direction unless in intersections.
        """
        __map = {
            Orientation2D.HORIZONTAL: {
                "0": Action2D.WEST,
                "1": Action2D.EAST
            },
            Orientation2D.VERTICAL: {
                "0": Action2D.NORTH,
                "1": Action2D.SOUTH
            }
        }
        return __map[self.orientation][self.dir]

class Corridor2D:
    """
    A class representing a Corridor in a 2D Map.
    Contains multiple channels. Drones can only be in one channel at a time unless in an intersection.
    """
    def __init__(self, orientation: Orientation2D, x: int, y: int, length: int, width: int, dir: Action2D):
        """
        If a Corridor is added into a map file as:
            CORRIDOR H 0 9 20 2 1

        Corridor direction is Horizontal.
        Corridor start coordinate is (0, 9).
        Corridor length is 20.
        Corridor has 2 channels.
        The direction value is 1.

        Since there are 2 corridors, we will convert this into a 2 digit binary number: 01
        Since this is a horizontal corridor, channels can only have EAST or WEST directions.

        Channel at index 0 will have direction associated with 0 () and channel at index 1 will have direction associated with 1 ().
        """
        self.orientation: Orientation2D = orientation
        """
        Represents the orientation of the corridor.
        """
        self.x: int = x
        """
        The x coordinate of the top left point of the corridor.
        """
        self.y: int = y
        """
        The y coordinate of the top left point of the corridor.
        """
        self.length: int = length
        """
        The length of the corridor.
        """
        self.width: int = width
        """
        The width of the corridor.
        """
        dir_parsed = f'{dir:0{width}b}'
        self.channels: "list[Channel2D]" = [Channel2D(i, dir_parsed[i], self.orientation) for i in range(width)]
        """
        A list of all the channels in the corridor.
        """

    def getRectangle(self) -> tuple[int, int, int, int]:
        """
        returns the rectangle containing the entire corridor.
        """
        return (self.x, self.y, self.length if self.orientation == Orientation2D.HORIZONTAL else self.width, self.width if self.orientation == Orientation2D.HORIZONTAL else self.length)

    def intersects(self, other: Corridor2D) -> bool:
        """
        checks if 2 corridors intersect.
        """
        rect1 = self.getRectangle()
        rect2 = other.getRectangle()
        return not (
            rect1[0] > rect2[3] or rect2[0] > rect1[3]
            or
            rect1[2] > rect2[4] or rect2[2] > rect1[4]
        )
    
    def getIntersectionBounds(self, other: Corridor2D) -> tuple(int, int, int, int):
        """
        returns the rectangle representing the intersection of 2 corridors.
        """
        if not self.intersects(other):
            rect1 = self.getRectangle()
            rect2 = other.getRectangle()
            left = max(rect1[0], rect2[0])
            top = max(rect1[1], rect2[1])
            right = min(rect1[0] + rect1[2], rect2[0] + rect2[2])
            bottom = min(rect1[1] + rect1[3], rect2[1] + rect2[3])
            return (left, top, right - left, bottom - top)

    def render(self, zIdx: int):
        """
        Draws the corridor onto the screen.
        """
        for l_offset in range(self.length):
            for channel in self.channels:
                if self.orientation == Orientation2D.HORIZONTAL:
                    drawAlphaCoordBlock(
                        self.x + l_offset,
                        self.y + channel.idx,
                        color=(*(
                            RED if channel.idx else GREEN
                        ), alphaFromZ(zIdx))
                    )
                elif self.orientation == Orientation2D.VERTICAL:
                    drawAlphaCoordBlock(
                        self.x + channel.idx,
                        self.y + l_offset,
                        color=(*(
                            PURPLE if channel.idx else BLUE
                        ), alphaFromZ(zIdx))
                    )
    def has(self, x: int, y: int) -> bool:
        """
        Checks that the given coordinates are inside the corridor.
        """
        return has(x, y, *self.getRectangle())

    def get_containing_channel(self, x: int, y: int) -> Channel2D:
        """
        returns the channel containing the given coordinate.
        """
        if self.has(x, y):
            if self.orientation == Orientation2D.HORIZONTAL:
                return self.channels[y - self.y]
            elif self.orientation == Orientation2D.VERTICAL:
                return self.channels[x - self.x]


class Intersection:
    """
    A class representing an intersection in 2D.
    """
    def __init__(self, corridor1: Corridor2D, corridor2: Corridor2D, intersectionRect: tuple[int, int. int. int]):
        [self.x, self.y, self.length, self.breadth] = intersectionRect
        """
        x: the x coordinate of the top left point of the intersection.
        y: the y coordinate of the top left point of the intersection.
        length: the length of the intersection.
        breadth: the breadth of the intersection.
        """
        self.corridor1: Corridor2D = corridor1
        """
        The first corridor this intersection is a part of.
        """
        self.corridor2: Corridor2D = corridor2
        """
        The second corridor this intersection is a part of.
        """

    def has(self, x: int, y: int) -> bool:
        """
        Checks if an intersection contains the given x, y coordinates.
        """
        return has(x, y, self.x, self.y, self.length, self.breadth)

    def render(self, zIdx: int):
        """
        Draws the intersection on the map.
        """
        for x in range(self.x, self.x + self.length):
            for y in range(self.y, self.y + self.breadth):
                drawAlphaCoordBlock(x, y, color=(*GRAY, alphaFromZ(zIdx)))

class Map2D:
    """
    A class representing a 2D Map.
    TODO: 2 ways of keeping track of a map: sparse and aircell. Currently Sparse implemented.
    """
    def __init__(self):
        self.corridors: "list[Corridor2D]" = []
        """
        A list of all corridors in this map.
        """
        self.dimension: "Dimension2D" = Dimension2D(0, 0)
        """
        The Dimensions of this map.
        """
        self.intersections: "list[Intersection]" = []
        """
        A list of all the intersections of the map.
        """
        self.drones_states: "list[DroneState]" = []
        """
        A list of all the drone states present on the map.
        """
        self.agent: Agent = ForwardDroneAgent()
        """
        The agent controlling the drone states on the map.
        """
        self.dispatchers: "list[DispatchVertiport]" = []
        """
        A list of all the dispatcher vertiports in the map.
        """
        self.goals: "dict[ReceiveVertiport, list[DroneState]]" = dict()
        """
        A dictionary mapping all receiving vertiports to all drones that have that vertiport's coordinates as a goal.
        """
        self.comms: CommunicationFabric = CommunicationFabric()
        """
        The communication fabric on this map.
        """
        self.mems: "dict[str, MemoryContext]" = dict()
        """
        The memory of all drones on this map.
        TODO: encapsulate in drone state
        """

    def has(self, x: int, y: int) -> bool:
        """
        checks if this given x, y coordinate is in the map bounds.
        """
        return has(x,y, 0, 0, self.dimension.width, self.dimension.height)
        
    def get_containing_corridor(self, x: int, y: int) -> Corridor2D:
        """
        given an x, y coordinate, returns the corridor that would contain this coordinate or else returns None.
        """
        for corridor in self.corridors:
            if corridor.has(x, y):
                return corridor

    def get_containing_intersection(self, x: int, y: int) -> Intersection2D:
        """
        given an x, y coordinate, returns the intersection that would contain this coordinate or else returns None.
        """
        for intersection in self.intersections:
            if intersection.has(x, y):
                return intersection

    def update_intersections(self):
        """
        Called to compute all the intersections on the map given the corridors on this map.
        """
        self.intersections = []
        for (a, b) in combinations(self.corridors, 2):
            intersectionBounds = a.getIntersectionBounds(b)
            if intersectionBounds:
                self.intersections += [Intersection(a, b, intersectionBounds)]
    
    def to_arr(self) -> list[list[str]]:
        """
        Converts the map to an array representation.
        TODO: describe representation.
        """
        map_base = [["O" for _ in range(self.dimension.width)] for _ in range(self.dimension.height)]
        for corridor in self.corridors:
            if corridor.orientation == Orientation2D.HORIZONTAL:
                for channel in corridor.channels:
                    for i in range(corridor.length):
                        map_base[corridor.y + channel.idx][i + corridor.x] += "<" if channel.dir == "0" else ">"
            elif corridor.orientation == Orientation2D.VERTICAL:
                for channel in corridor.channels:
                    for i in range(corridor.length):
                        map_base[i + corridor.y][corridor.x + channel.idx] += "v" if channel.dir == "1" else "^"
        for intersection in self.intersections:
            for i in range(intersection.length):
                for j in range(intersection.breadth):
                    map_base[intersection.y + j][intersection.x + i] += "@"
        
        return map_base

    def render(self, zIdx: int):
        """
        Draws the map onto the screen.
        """
        for x in range(self.dimension.width):
            for y in range(self.dimension.height):
                drawAlphaCoordBlock(x, y)

        for corridor in self.corridors:
            corridor.render(zIdx + 1)
        
        for intersection in self.intersections:
            intersection.render(zIdx + 1)

        for drone in self.drones_states:
            drone.render(zIdx + 1)

        for dispatcher in self.dispatchers:
            dispatcher.render(zIdx + 1)

        for x in range(self.dimension.width):
            for y in range(self.dimension.height):
                drawCoordBlock(x, y, color=(*WHITE, alphaFromZ(zIdx)), border=1)
                corridor = self.get_containing_corridor(x, y)
                if corridor:
                    channel = corridor.get_containing_channel(x, y)
                    if channel and not self.get_containing_intersection(x, y):
                        drawArrow(x, y, channel.getDirection())

    def validDroneSpot_drones(self, x, y, nearestDroneThreshold = 2):
        # TODO: check the +1 for upper limit
        for drone in self.drones_states:
            if (
                drone.getCoords().x - nearestDroneThreshold < x and drone.getCoords().x + nearestDroneThreshold + 1 > x 
            and drone.getCoords().y - nearestDroneThreshold < y and drone.getCoords().y + nearestDroneThreshold + 1 > y
            ): return False
        
        return True

    def update(self):
        """
        Updates all the components on the map.
        """
        for drone_state in self.drones_states:
            if  drone_state.goal in self.goals and drone_state.goal.has(drone_state.getCoords().x, drone_state.getCoords().y):
                drone_state.goal.receive(drone_state)
                self.goals[drone_state.goal] = list(filter(lambda e: e != drone_state, self.goals[drone_state.goal]))
                self.drones_states = list(filter(lambda e: e != drone_state, self.drones_states))
                continue
            if drone_state.id not in self.mems:
                self.mems[drone_state.id] = MemoryContext()
            drone_state.applyAction(self.agent.getAction((DroneStateContext(drone_state, self.mems[drone_state.id]), DroneSimContext(drone_state, self))))
            # TODO: have drone push message onto fabric
        
        for dispatcher in self.dispatchers:
            if self.validDroneSpot_drones(dispatcher.x, dispatcher.y):
                dispatched_drone = dispatcher.dispatch()
                if dispatched_drone:
                    self.drones_states += [dispatched_drone]
                dispatcher.update()
        
        self.comms.update()

    def set_global_agent(self, agent: DroneAgent):
        """
        Changes the Agents controlling each drone on the simulation.
        """
        if isinstance(agent, DroneAgent):
            self.agent = agent
        elif issubclass(agent, DroneAgent):
            self.agent = agent()
    
    def apply_simulation_settings(self, settings):
        """
        Applies the given settings onto the simulation.
        TODO: describe the settings dict.
        """
        _SIMULATION_SETTINGS_LOOKUP = {
            "global-agent": lambda e: self.set_global_agent(e)
        }

        for key in settings:
            if key in _SIMULATION_SETTINGS_LOOKUP:
                _SIMULATION_SETTINGS_LOOKUP[key](settings[key])

    def shutdown(self, drone: DroneState):
        """
        Shuts down the drone and removes it from the map (if not called here it will still be on the map and will be an error). Furthermore there might be a mem leak.
        """
        if drone in self.drones_states:
            drone.shutdown()
            if drone.id in self.mems:
                del self.mems[drone.id]
            self.drones_states.remove(drone)

