# forward declare types
from __future__ import annotations

from UTM.agents import DroneAgent
from UTM.comms import Packet, PacketHeader
from UTM.constants import Action2D, DroneSimContext
from UTM.drone import DroneStateContext
from UTM.kpi_utils import DataSink

import pandas as pd

from functools import cmp_to_key as keyify

class CommunicationCapableAgent(DroneAgent):
    """
    A simple agent to show how Drone communication will work using the dispatch/ fetch (push/ pull) mechanism.
    Fetching is done outside the agent, assumed to be an abstraction of the drone's communication drivers.
    env_context has a comms_buffer that will contain all Packet instances relevant to this drone.

    At the moment, if a packet has a drone_id different from the Drone the Agent is working on, it is relevant 
    to the current Drone. However, in later versions of the simulation, there should be a feature to 
    modify which packet the driver can pick up and allow the drone to fetch for the agent. #TODO
    """
    def getAction(self, state: tuple[DroneStateContext, DroneSimContext]) -> Action2D:
        drone_context, env_context = state
        """
        Demonstration of fact that the env_context.comms_buffer contains a list of packets
        """
        # print([packet.header.source_id for packet in env_context.comms_buffer])

        """
        Demonstration of how to dispatch packets. These will be available for the next iteration.
        PacketHeader is information that is uniform across all packets, sent by not just this drone but all drones.
        For the sake of real world mapping, rather than extend Packet Header, modify the original class 
            -> This will be analogous to a "software update" on all drones allowing them to read the same type of packeting scheme.
        
        Packet Communication Protocol should allow for a bootstrapping of versions, so that a drone with an 
        older version driver can understand some content of the packet sent by a newer version
        Check with Dr Namuduri if this is a required implementation within scope or more in the scope of network protocol #TODO
        """
        env_context.dispatch (
            Packet (
                PacketHeader (
                    drone_context.id
                ),
                [
                    f"Pos: {drone_context.x}, {drone_context.y}",
                    {"Did you know that:": "this data can be anything that implements __str__ for the simulation's sake"}
                ]
            )
        )
        """
        Continue moving along the same direction
        """
        return drone_context.dir
#TODO: maybe don't call this an agent
class TurnRightAtIntersectionAgent(DroneAgent):
    """
    A simple agent that is slightly more advanced than the inbuilt ForwardDroneAgent. 
    This one will detect when we are in an intersection and automatically move right.
    Please use maps/intersection-right.map with this agent to prevent crashes due to drones not 
    reaching the goal. 

    When we enter the intersection, we will need to just turn right.
    """
    def getAction(self, state: tuple[DroneStateContext, DroneSimContext]) -> Action2D:
        drone_context, env_context = state
        """
        Simple method just checks if our drone is in any intersection.
        An alternative could be to just use:
        env_context.get_containing_intersection(drone_context.x, drone_context.y) is not None
        since DroneSimContext.get_containing_intersection will only return None when it is not in an intersection
        """
        isInIntersection = any([
            intersection.has(drone_context.x, drone_context.y)
            for intersection in env_context.intersections
        ])

        """
        If we are in an intersection, we lookup which Direction is the "RIGHT" direction of the one
        we are currently on. 
        """
        if isInIntersection:
            return Action2D.RIGHT[drone_context.dir]

        """
        If we are not in an intersection, we will continue moving along the same direction.
        """
        return drone_context.dir

class TurnLeftAtIntersectionAgent(DroneAgent):
    """
    A complex agent that is slightly more advanced than the TurnRightAtIntersectionAgent. 
    This one will detect when we are in an intersection and automatically move left.
    Please use maps/intersection-left.map with this agent to prevent crashes due to drones not 
    reaching the goal. 

    In the map, to turn left at the intersection, our drone needs to make sure that it 
    comes out on the correct channel. 
    If we are going in from the "Bottom" "East" Channel, the drone must come out through the "Right" "North" Channel.

             | X | ^ |
    Drone -> | > | ^ |

    This is because immediately turning left into an intersection will result in:

             | ^ | X |
    Drone -> | ^ | X |

    however, we now see that the drone is moving North along a South Channel. This will be illegal in the simulation.

    This means that it must make a long turn at the intersection, which needs to be done in 3 iterations:

    To achieve this functionality, we will be using the memory the simulation provides each Drone.


    We can do this by mimicing a state machine to keep track of where we are in the intersection.
    I have simplified the intesection to use a list keeping track of whether we were in an 
    intersection in the last 3 simulation states.

    If the last 2 simulation states were in an intersection, we turn left. Otherwise we move forward.
    This forces a long turn.

    """
    def getAction(self, state: tuple[DroneStateContext, DroneSimContext]) -> Action2D:
        drone_context, env_context = state
        """
        This line just checks if the drone is in an intersection.
        DroneSimContext.get_containing_intersection will only return None when the drone is not in an intersection
        """
        isInIntersection = env_context.get_containing_intersection(drone_context.x, drone_context.y) is not None
        """
        This if statement is true when our drone has just started out. 
        We need to make sure that all memory is initialized.
        Since we have only one variable, we can have a simple guard statement.

        If we plan on having multiple variables, we can have a "flag" in memory, and if that flag is not set
        then we can initialize all the variables.

        The goal is to eventually not require this guard variable. I am debating for now allowing
        variables that do not exist to return None. #TODO
        """
        if not "intersectionHistory" in drone_context.mem:
            """
            Since our drone has just started, we initialize the last 3 states to be False, False, False meaning
            we were not in an intersection 3 iterations ago.
            """
            drone_context.mem.intersectionHistory = [False, False, False]

        """
        This line adds the current cycle's interesection state into the history list we have,
        then it truncates the list to only keep the latest 3 intersections states.
        """
        drone_context.mem.intersectionHistory = ([isInIntersection] + drone_context.mem.intersectionHistory)[:3]

        """
        If the last 2 intersection states were True and the 3rd (or latest stored history) state was false,
        we have to turn left!
        """
        if all(drone_context.mem.intersectionHistory[:-1]) and not drone_context.mem.intersectionHistory[-1]:
            return Action2D.LEFT[drone_context.dir]

        """
        In all other cases, we just need to go forward in the direction we were going.
        """
        return drone_context.dir

class DFSAgent(DroneAgent):
    """
    TODO: basic DFS implementation to show how to check legality of steps and perform known algos 
    TODO: demonstrate that storing data at the agent level is a mem leak -> will never get cleared.
    """
    def getAction(self, state: tuple[DroneStateContext, DroneSimContext]) -> Action2D:
        drone_context, env_context = state
        raise Exception("Unimplemented agent.")

class BFSAgent(DroneAgent):
    """
    TODO: ask ananay for description, since it has not been put on the github rn.
    """
    def getAction(self, state: tuple[DroneStateContext, DroneSimContext]) -> Action2D:
        drone_context, env_context = state
        raise Exception("Unimplemented agent.")

class AStarAgent(DroneAgent):
    """
    TODO: ask ananay for description, since it has not been put on the github rn.
    """
    def getAction(self, state: tuple[DroneStateContext, DroneSimContext]) -> Action2D:
        drone_context, env_context = state
        raise Exception("Unimplemented agent.")

class DjikstrasAgent(DroneAgent):
    """
    TODO: ask ananay for description, since it has not been put on the github rn.
    """
    def getAction(self, state: tuple[DroneStateContext, DroneSimContext]) -> Action2D:
        drone_context, env_context = state
        raise Exception("Unimplemented agent.")

class IntersectionQueueResolverAgent(DroneAgent):
    """
    TODO: time at intersection? should drones who have been waiting for a while be given priority?
    """
    def __init__(self):
        self.threshold = 4
        self.intersection_delay_sink = DataSink("intersection_delay", plotter=lambda ax, **kwargs1: lambda xs, ys, **kwargs2: ax.hist(ys))
        self.traffic_delay_sink = DataSink("traffic_delay", plotter=lambda ax, **kwargs1: lambda xs, ys, **kwargs2: ax.hist(ys))
        self.traffic_smoothness_sink = DataSink("traffic_smoothness", plotter=lambda ax, **kwargs1: lambda xs, ys, **kwargs2: ax.hist(ys))
        def traffic_smoothness_calculator(xs, ys, colors):
            df = pd.DataFrame({'y': ys, 'id': xs})
            df = df.groupby(['id']).std().reset_index()
            return df['id'], df['y']
        self.traffic_smoothness_sink.preprocess = traffic_smoothness_calculator

    def getAction(self, state: tuple[DroneStateContext, DroneSimContext]) -> Action2D:
        # this is not what we described in the protocol we made, it is a fix -> 
        # basically instead of at the beginning of a simulation cycle we broadcast the current position
        # at the end of the cycle we broadcast the position that will be the next position (intent instead of actual)
        # this prevents drones from thinking the intersection is unlocked when actually another drone intended to go inside
        # rising edge vs falling edge position update ( i feel like this is more expensive in the real world )
        action = self._computeAction(state)
        newX, newY = state[0].x, state[0].y
        if action == Action2D.EAST:
            newX += 1
        if action == Action2D.WEST:
            newX -= 1
        if action == Action2D.NORTH:
            newY -= 1
        if action == Action2D.SOUTH:
            newY += 1
        self.broadcast_packets(state[0].id, {"x": newX, "y": newY, "intersectionDelay": state[0].mem["intersectionDelay"]}, state[1].dispatch)
        
        self.traffic_smoothness_sink.update(state[0].id, 0 if action == Action2D.NOP else 1)

        
        self.intersection_delay_sink.save()
        self.traffic_delay_sink.save()
        self.traffic_smoothness_sink.save()
        # print("Drone result:", state[0].id, action)
        return action

        
    def _computeAction(self, state: tuple[DroneStateContext, DroneSimContext]) -> Action2D:
        drone_context, env_context = state
        # TODO: i think drones are keeping track of older drones? do we need this? causes a stall/ buildup
        if "droneMap" not in drone_context.mem or True:
            drone_context.mem["droneMap"] = dict()

        if "intersectionDelay" not in drone_context.mem:
            drone_context.mem["intersectionDelay"] = 0

        if "trafficDelay" not in drone_context.mem:
            drone_context.mem["trafficDelay"] = 0

        # Rule: drones listen to env and get RID data 
        for i in env_context.comms_buffer:
            if "x" in i.data and "y" in i.data:
                drone_context.mem["droneMap"][i.header.source_id] = i.data

        # Rule: if 2 prisms ahead of the current drone has another drone, current drone halts till the spot is free
        for i in drone_context.mem["droneMap"]:
            if i == drone_context.id:
                continue
            if drone_context.dir == Action2D.EAST or drone_context.dir == Action2D.WEST:
                if abs(drone_context.mem["droneMap"][i]["x"] - drone_context.x) <= 2  and drone_context.mem["droneMap"][i]["y"] == drone_context.y:
                    if drone_context.dir == Action2D.EAST and drone_context.x < drone_context.mem["droneMap"][i]["x"]:
                        drone_context.mem["trafficDelay"] += 1
                        self.traffic_delay_sink.update(drone_context.id, drone_context.mem["trafficDelay"])
                        return Action2D.NOP
                    elif drone_context.dir == Action2D.WEST and drone_context.x > drone_context.mem["droneMap"][i]["x"]:
                        drone_context.mem["trafficDelay"] += 1
                        self.traffic_delay_sink.update(drone_context.id, drone_context.mem["trafficDelay"])
                        return Action2D.NOP
            if drone_context.dir == Action2D.NORTH or drone_context.dir == Action2D.SOUTH:
                if abs(drone_context.mem["droneMap"][i]["y"] - drone_context.y) <= 2  and drone_context.mem["droneMap"][i]["x"] == drone_context.x:
                    if drone_context.dir == Action2D.NORTH and drone_context.y > drone_context.mem["droneMap"][i]["y"]:
                        drone_context.mem["trafficDelay"] += 1
                        self.traffic_delay_sink.update(drone_context.id, drone_context.mem["trafficDelay"])
                        return Action2D.NOP
                    elif drone_context.dir == Action2D.SOUTH and drone_context.y < drone_context.mem["droneMap"][i]["y"]:
                        drone_context.mem["trafficDelay"] += 1
                        self.traffic_delay_sink.update(drone_context.id, drone_context.mem["trafficDelay"])
                        return Action2D.NOP

        # Rule: When the current drone enters a threshold prism in the intersection, it will listen for RID data from all drones in that threshold distance at all lanes from that intersection 
        #           The threshold is with respect to the center of intersection 
        # TODO: make for n number of intersections
        # TODO: the above rule was not correctly worded as drone is always looking for RID data for the 2 prism distance rule
        intersection = env_context.intersections[0]
        intersection_center = (
            intersection.x + (intersection.breadth / 2),
            intersection.y + (intersection.length / 2)
        )
        if self.distance(drone_context.x, drone_context.y, *intersection_center) <= 3 and not self.hasMovedOutOfIntersection(drone_context, intersection):
            rank = self.computeQueuePosition(drone_context, intersection_center)
            drone_context.mem["intersectionDelay"] += 1
            self.intersection_delay_sink.update(drone_context.id, drone_context.mem["intersectionDelay"])
            if rank != 0 or self.isIntersectionLocked(intersection, drone_context.mem["droneMap"], drone_context):
                # path planning kicks in during the intersection
                return Action2D.NOP
        return drone_context.dir

    def hasMovedOutOfIntersection(self, drone_context: DroneStateContext, intersection):
        if drone_context.dir == Action2D.NORTH:
            return drone_context.y < intersection.y
        if drone_context.dir == Action2D.SOUTH:
            return drone_context.y > intersection.y + intersection.length - 1
        
        if drone_context.dir == Action2D.WEST:
            return drone_context.x < intersection.x
        if drone_context.dir == Action2D.EAST:
            return drone_context.x > intersection.x + intersection.breadth - 1

    def computeQueuePosition(self, drone_context: DroneStateContext, intersection_center):
        #TODO: get type incorporated
        # no drones
        if "droneMap" not in drone_context.mem:
            return 0
        if len(drone_context.mem["droneMap"].keys()) < 2:
            return 0
        
        queue = [{"id": i, "x": drone_context.mem["droneMap"][i]["x"], "y": drone_context.mem["droneMap"][i]["y"], "intersectionDelay": drone_context.mem["droneMap"][i]["intersectionDelay"]} for i in drone_context.mem["droneMap"]]
        queue += [{"id": drone_context.id, "x": drone_context.x, "y": drone_context.y, "intersectionDelay": drone_context.mem["intersectionDelay"]}]
        def compareDrones(drone1, drone2):
            distance_diff = self.distance(drone1["x"], drone1["y"], *intersection_center) - self.distance(drone2["x"], drone2["y"], *intersection_center)
            
            ## TODO: get number of current drones incorporated
            
            time_diff = drone1["intersectionDelay"] - drone2["intersectionDelay"]
            if time_diff < 0:
                return drone1
            if time_diff > 0:
                return drone2
            
            # if distance_diff < 0:
            #     return drone1
            # if distance_diff > 0:
            #     return drone2


            if drone1["id"] < drone2["id"]:
                return drone1
            return drone2

        queue = sorted(queue, key=keyify(lambda x, y : +1 if compareDrones(x, y) == x else -1))
        # print("queue for ", drone_context.id, " is ", queue)
        for i in range(len(queue)):
            if queue[i]["id"] == drone_context.id:
                return i
        return len(queue)

    def isIntersectionLocked(self, intersection, droneMap, drone_context):
        for i in droneMap:
            if i == drone_context.id:
                continue
            if intersection.has(droneMap[i]["x"], droneMap[i]["y"]):
                return True
        return False



        
    #TODO: this seems to be ruining the intersection model - cannot use euclidean distance!!
    def distance(self, x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

                

    def broadcast_packets(self, id, data: any, dispatcher):
        dispatcher(
            Packet (
                PacketHeader (
                    id
                ),
                data
            )
        )


EXPORT = {
    "simulation-settings": {
        "global-agent": IntersectionQueueResolverAgent
    },
    "main": {
        "map-file": "maps/intersection-queue.map",
        "strict-verify": "simple"
    }
}