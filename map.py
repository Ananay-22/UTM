from enum import Enum
from itertools import combinations
from agents import Agent, DroneAgent, ForwardDroneAgent
from comms import CommunicationFabric

from constants import BLUE, GRAY, GREEN, PURPLE, RED, WHITE, Dimension2D, DroneSimContext, Orientation2D
from computed import alphaFromZ
from dispatcher import DispatchUnit, ReceiveUnit
from drone import Action2D, DroneState, DroneStateContext, MemoryContext

from render_util import drawAlphaCoordBlock, drawArrow, drawCoordBlock
from utils import has

class Channel2D:
    def __init__(self, idx, dir, orientation):
        self.idx = idx
        self.dir = dir
        self.orientation = orientation
    
    def getDirection(self):
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
    def __init__(self, orientation, x, y, length, width, dir):
        self.orientation = orientation
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        dir_parsed = f'{dir:0{width}b}'
        self.channels = [Channel2D(i, dir_parsed[i], self.orientation) for i in range(width)]

    def getRectangle(self):
        return (self.x, self.y, self.length if self.orientation == Orientation2D.HORIZONTAL else self.width, self.width if self.orientation == Orientation2D.HORIZONTAL else self.length)

    def intersects(self, other):
        rect1 = self.getRectangle()
        rect2 = other.getRectangle()
        return not (
            rect1[0] > rect2[3] or rect2[0] > rect1[3]
            or
            rect1[2] > rect2[4] or rect2[2] > rect1[4]
        )
    
    def getIntersectionBounds(self, other):
        if not self.intersects(other):
            rect1 = self.getRectangle()
            rect2 = other.getRectangle()
            left = max(rect1[0], rect2[0])
            top = max(rect1[1], rect2[1])
            right = min(rect1[0] + rect1[2], rect2[0] + rect2[2])
            bottom = min(rect1[1] + rect1[3], rect2[1] + rect2[3])
            return (left, top, right - left, bottom - top)

    def render(self, zIdx):
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
    def has(self, x, y):
        return has(x, y, *self.getRectangle())

    def get_containing_channel(self, x, y):
        if self.has(x, y):
            if self.orientation == Orientation2D.HORIZONTAL:
                return self.channels[y - self.y]
            elif self.orientation == Orientation2D.VERTICAL:
                return self.channels[x - self.x]


class Intersection:
    def __init__(self, corridor1, corridor2, intersectionRect):
        [self.x, self.y, self.length, self.breadth] = intersectionRect
        self.corridor1 = corridor1
        self.corridor2 = corridor2

    def has(self, x, y):
        return has(x, y, self.x, self.y, self.length, self.breadth)

    def render(self, zIdx):
        for x in range(self.x, self.x + self.length):
            for y in range(self.y, self.y + self.breadth):
                drawAlphaCoordBlock(x, y, color=(*GRAY, alphaFromZ(zIdx)))

class Map2D:
    def __init__(self):
        self.corridors: list[Corridor2D] = []
        self.dimension: Dimension2D = Dimension2D(0, 0)
        self.intersections: list[Intersection] = []
        self.drones_states: list[DroneState] = []
        self.agent: Agent = ForwardDroneAgent()
        self.dispatchers: list[DispatchUnit] = []
        self.goals: dict[ReceiveUnit, list[DroneState]] = dict()
        self.comms: CommunicationFabric = CommunicationFabric()
        self.mems: dict[str, MemoryContext] = dict()

    def has(self, x, y):
        return has(x,y, 0, 0, self.dimension.width, self.dimension.height)
        
    def get_containing_corridor(self, x, y) -> Corridor2D:
        for corridor in self.corridors:
            if corridor.has(x, y):
                return corridor

    def get_containing_intersection(self, x, y):
        for intersection in self.intersections:
            if intersection.has(x, y):
                return intersection

    def update_intersections(self):
        for (a, b) in combinations(self.corridors, 2):
            intersectionBounds = a.getIntersectionBounds(b)
            if intersectionBounds:
                self.intersections += [Intersection(a, b, intersectionBounds)]
    
    def to_arr(self):
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

    def render(self, zIdx):
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


    def update(self):
        for drone_state in self.drones_states:
            if  drone_state.goal in self.goals and drone_state.goal.has(drone_state.getCoords().x, drone_state.getCoords().y):
                drone_state.goal.receive(drone_state)
                self.goals[drone_state.goal] = list(filter(lambda e: e != drone_state, self.goals[drone_state.goal]))
                self.drones_states = list(filter(lambda e: e != drone_state, self.drones_states))
                continue
            if drone_state.id not in self.mems:
                self.mems[drone_state.id] = MemoryContext()
            drone_state.applyAction(self.agent.getAction(DroneStateContext(drone_state, self.mems[drone_state.id]), DroneSimContext(drone_state, self)))
            # TODO: have drone push message onto fabric
        
        for dispatcher in self.dispatchers:
            dispatched_drone = dispatcher.dispatch()
            if dispatched_drone:
                self.drones_states += [dispatched_drone]
            dispatcher.update()
        
        self.comms.update()

    def set_global_agent(self, agent: DroneAgent):
        if isinstance(agent, DroneAgent):
            self.agent = agent
        elif issubclass(agent, DroneAgent):
            self.agent = agent()
    
    def apply_simulation_settings(self, settings):
        _SIMULATION_SETTINGS_LOOKUP = {
            "global-agent": lambda e: self.set_global_agent(e)
        }

        for key in settings:
            if key in _SIMULATION_SETTINGS_LOOKUP:
                _SIMULATION_SETTINGS_LOOKUP[key](settings[key])

    def shutdown(self, drone: DroneState):
        if drone in self.drones_states:
            drone.shutdown()
            if drone.id in self.mems:
                del self.mems[drone.id]
            self.drones_states.remove(drone)

