from drone import DroneType
from agents import DroneAgent
class Cell:
    """
    Represents a single unit on the map.
    TODO: integrate with simulation. 
    """
    def __init__(self):
        """
            Represents rainfall in mm.
            TODO: check rainfall requirements (light rainfall should be okay with most drones).
        """
        self.rainfall = 0
        """
            Represents temperature in degrees C
            If it is not in the range 40F < temperature < 80F  then the drone would 
            have to activate self landing (known location nearest to the current location)
            # ideal temperature -> 60F
        """
        self.temperature = 25
        """
            Represents windspeed in 
            TODO: check on windspeed that would affect drone (drone speed - 10 mph)
            TODO: check the windspeed is managed as a vector (for directionality)
        """
        self.windspeed = [0, 0]

        # TODO: snowfall/ hailstorm??


    """
        Returns the probability of a drone moving into this cell. [0, 1] 
    """
    def get_environment_potential(self, drone_type: DroneType):
        # rainfall_potential * temp_potential * wind_potential
        pass

    def get_path_potential(self):
        pass



class AirCell(Cell):
    """
    AirCells are the units on the map that a drone can occupy.
    TODO: complete and integrate with simulation. Follow up with Saanvi
    """
    def __init__(self) :
        self.drone = None

    def is_empty(self) :
        return self.drone == None

    def add_drone(self, drone: DroneAgent):
        if not self.drone:
            self.drone = drone

def get_aircell_potential(cell: AirCell, surrounding_cell: list[AirCell]) -> float:
    """
    This method is redundant, should be encapsulated in the right part of the simulation.
    """
    return 0.0
