import pygame
from UTM.drone import DroneState
from UTM.loader import loadMaps
from UTM.map import Map2D
from UTM.render_util import drawAlphaRect
from time import sleep, time
from UTM.constants import *
from UTM.utils import blockPositiontoGridIndex
from UTM.render_util import SCREEN, CLOCK
from UTM.kpi_utils import DataSink
import sys

class SimulationController:
    def __init__(self):
        self.sim_speed = 1
        self.play = False
        # TODO: make screen and clock here so it can be passed into the SimulationState

def render(SimulationState):
    global SCREEN
    SCREEN.fill(BLACK)
    SimulationState.render(1)
    pygame.display.update()

def input(SimulationState: Map2D, controller: SimulationController):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x, y = x // 32, y // 32
            if SimulationState.get_containing_corridor(x, y):
                keys = pygame.key.get_pressed()
                action = list(map(lambda e: pygame.key.name(e), filter(lambda e: keys[e], [pygame.K_n, pygame.K_s, pygame.K_w, pygame.K_e, pygame.K_o])))
                if len(action) > 0:
                    SimulationState.drones_states += [DroneState(MovementVector2D(x, y, Action2D(action[0].upper())))]



            else:
                print("DRONE CANNOT BE SPAWNED OUTSIDE THE CORRIDOR")
            return
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                controller.play = not controller.play

            if event.key == pygame.K_SEMICOLON:
                controller.sim_speed = min(30, controller.sim_speed + 1)
            if event.key == pygame.K_l:
                controller.sim_speed = max( 1, controller.sim_speed - 1)

def update(SimulationState):    
    SimulationState.update()

def cleanup(SimulationState: Map2D):  
    list(map(lambda e: SimulationState.shutdown(e), filter(lambda e: (not SimulationState.has(e.getCoords().x, e.getCoords().y)) and not e.goal, SimulationState.drones_states)))
    # SimulationState.drones_states = list(filter(lambda e: not((not SimulationState.has(e.getCoords().x, e.getCoords().y)) and not e.goal), SimulationState.drones_states))

# _prev_drone_states = {}
def verify(SimulationState: Map2D, strict = False):
    # raise Exception("Something went wrong...")
    # global _prev_drone_states
    # check if a drone moved off the map and that was not the goal
    if (not all([SimulationState.has(drone.getCoords().x, drone.getCoords().y) or not drone.goal for drone in SimulationState.drones_states])):
        raise Exception("A drone was out of the SimulationState")
    
    # check drones are all in corridors
    if (not all([SimulationState.get_containing_corridor(drone.getCoords().x, drone.getCoords().y) for drone in SimulationState.drones_states])):
        raise Exception("A drone has moved out of the corridors")

    # check that drones are updating in channel directions??
    if (not all([
        SimulationState.get_containing_intersection(drone.getCoords().x, drone.getCoords().y)
        or drone.getDirection() in [SimulationState.get_containing_corridor(
            drone.getCoords().x,
            drone.getCoords().y
        ).get_containing_channel(
            drone.getCoords().x,
            drone.getCoords().y
        ).getDirection(), Action2D.NOP]  for drone in SimulationState.drones_states
    ])):
        raise Exception("A drone did not follow it's channel's direction")

    if strict == "simple":
        for drone1 in SimulationState.drones_states:
            for drone2 in SimulationState.drones_states:
                if drone1 == drone2: continue
                if (drone1.getCoords().x == drone2.getCoords().x and drone1.getCoords().y == drone2.getCoords().y):
                    raise Exception("2 drones were in the same prism")
                if ((
                        SimulationState.get_containing_corridor(drone1.getCoords().x, drone1.getCoords().y).get_containing_channel(drone1.getCoords().x, drone1.getCoords().y)
                        ==
                        SimulationState.get_containing_corridor(drone2.getCoords().x, drone2.getCoords().y).get_containing_channel(drone2.getCoords().x, drone2.getCoords().y)
                    )
                    and
                    (
                        (abs(drone1.getCoords().x - drone2.getCoords().x) <= 1 and drone1.getCoords().y == drone2.getCoords().y)
                        or 
                        (abs(drone1.getCoords().y - drone2.getCoords().y) <= 1 and drone1.getCoords().x == drone2.getCoords().x)
                    )
                    and # required because drones can be < 2 distance at an intersection
                    (
                        SimulationState.get_containing_intersection(drone1.getCoords().x, drone1.getCoords().y) == None
                        and
                        SimulationState.get_containing_intersection(drone2.getCoords().x, drone2.getCoords().y) == None
                    )
                ):
                    raise Exception("2 drones were closer than <2 aircells")

        # for intersection in SimulationState.intersections:
        #     if [intersection.has(drone.getCoords().x, drone.getCoords().y) for drone in SimulationState.drones_states].count(True) > 1:
        #         raise Exception("2 drones were in the same intersection")

    # TODO: remove dependence on global variable -> shift resp. to SimulationState
    # if _prev_drone_states:
    #     curr_drone_states = {drone.id: drone for drone in SimulationState.drones_states}
    #     for curr_id in curr_drone_states:
    #         if curr_id in _prev_drone_states:
    #             curr_drone = curr_drone_states[curr_id]
    #             # at this point, you can compare the states between curr drone and prev drone
        
    #     _prev_drone_states = curr_drone_states
    


def run(SimulationState: Map2D, verifyRulesStrict = False):
    global SCREEN, CLOCK
    controller = SimulationController()

    kpi_sinks = [DataSink("simulation_runtime"), DataSink("drone_uptime")]

    [SimulationState.register_sink(i.name, i.update) for i in kpi_sinks]

    last = time()
    while True:
        render(SimulationState)
        input(SimulationState, controller)
        if time() - last > 1 / controller.sim_speed and controller.play:
            update(SimulationState)
            cleanup(SimulationState)
            last = time()
        verify(SimulationState, verifyRulesStrict)
        [i.save() for i in kpi_sinks]
        CLOCK.tick(60)

if __name__ == "__main__":
    from UTM.program import EXPORT
    if type(EXPORT) != dict or not "main" in EXPORT or not "map-file" in EXPORT["main"]:
        print("Program did not export correct settings!\nSimulation Cannot be programmed.")

    SimulationState: Map2D = loadMaps(EXPORT["main"]["map-file"])[0]
    
    if "simulation-settings" in EXPORT:
        SimulationState.apply_simulation_settings(EXPORT["simulation-settings"])
    # print(SimulationState.to_arr())
    run(SimulationState,
        verifyRulesStrict= EXPORT["main"]["strict-verify"] if "strict-verify" in EXPORT["main"] else False
        )

#TODO: Traffic model -> potential based moving