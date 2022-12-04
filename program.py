# forward declare types
from __future__ import annotations

from agents import DroneAgent
from comms import Packet, PacketHeader
from constants import Action2D, DroneSimContext
from drone import DroneStateContext

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
        print([packet.header.source_id for packet in env_context.comms_buffer])

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

EXPORT = {
    "simulation-settings": {
        "global-agent": TurnLeftAtIntersectionAgent
    },
    "main": {
        "map-file": "maps/intersection-left.map",
        "strict-verify": "simple"
    }
}