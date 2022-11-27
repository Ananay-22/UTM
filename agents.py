from comms import Packet, PacketHeader
from constants import DroneSimContext
from drone import DroneState, DroneStateContext

class Agent:
    def getAction(self, state):
        """
        Taking in a state, the agent should return the action to be taken.

        Agent: entity in a program or environment capable of generating action.
        An agent uses perception of the environment to make decisions about actions to take.
        The perception capability is usually called a sensor.
        The actions can depend on the most recent perception or on the entire history (percept sequence).
        
        https://www.cs.iusb.edu/~danav/teach/c463/3_agents.html
        """
        raise NotImplementedError("Agent's getAction() function has not been implemented: " + self)

class DroneAgent(Agent):
    """
    Drone Agents will be used to control the drones.
    They will take a DroneState in as a state (this state is it's perception capability or it's sensor).
    Drone States will have memory where the history can be stored.

    env_context will represent the state of the environment that the drone has sensed.
    """
    def getAction(self, drone_context: DroneStateContext, env_context: DroneSimContext):
        raise NotImplementedError("DroneAgent's getAction() function has not been implemented: " + self)

class ForwardDroneAgent(DroneAgent):
    """
    A specialized agent that can only move forward. 
    Not an ideal Agent, we want an intelligent one that can make decisions based on the contexts sensed.

    However this serves as a way to demonstrate how the Agent works since previous classes were abstract.
    Here the Agent just returns the Action as the current Drone Direction, therefore making the drone move forward.

    Ideally a drone will use the sensor data and depending on the state it will return an action (using conditionals and more advanced constructs).
    """
    def getAction(self, drone_context: DroneStateContext, env_context: DroneSimContext):
        return drone_context.dir