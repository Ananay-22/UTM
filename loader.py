# defining a map file format that is bound to change
# map constraints: air corridors are basically straight lines for now
# they are rectangles with a start coord, and a length, width
# start coord will specify where to start it (should not overlap)
# length specifies how long
# width specifies how many lanes, number after widths is read as 
# binary number where a 1 in the bit position specifies if the channel
# is moving away from start and 0 is moving towards start
# .<name> specifies name of section parser

# .2D
# DIM 20 20
# CORRIDOR H 0 9 20 2 2
# CORRIDOR V 9 0 20 2 2


from dispatcher import DispatchVertiport, ReceiveVertiport
from drone import DroneState
from map import Corridor2D, Map2D
from constants import Dimension2D, MovementVector2D, Orientation2D, Action2D

def tokenize(line):
    return line.split(" ")

def _2D_parser(lines):
    ret = Map2D()
    for line in lines[1:]:
        line = tokenize(line)
        if line[0] == ";":
            continue
        if line[0] == "DIM":
            ret.dimension = Dimension2D(*map(lambda s: int(s), line[1:]))
        if line[0] == "CORRIDOR":
            ret.corridors += [Corridor2D(Orientation2D(line[1]), *map(lambda s: int(s), line[2:]))]
        if line[0] == "DRONE":
            goal = ReceiveVertiport(int(line[6]), int(line[7])) if len(line) == 8 else None
            drone_state = DroneState(MovementVector2D(*map(lambda s: int(s), line[1:3]), Action2D(line[3])), line[4], int(line[5]), goal)
            if goal:
                if goal not in ret.goals:
                    ret.goals[goal] = []
                ret.goals[goal] += [drone_state]
            ret.drones_states += [drone_state]
        if line[0] == "DISPATCHER":
            #Todo: add generator, and receive unit support, random receive unit support too
            ret.dispatchers += [DispatchVertiport(int(line[1]), int(line[2]), Action2D(line[3]))]
    ret.update_intersections()
    return ret
parserLookup = {
    "2D": _2D_parser
}

def loadMaps(file):
    lines = []
    ret = []
    with open(file) as f:
        lines = [i.replace("\n", "") for i in f.readlines()]
    for i in range(len(lines)):
        line = lines[i]
        if line[0] == ";":
            continue
        if line[0] == ".":
           # forward lookup to see where section ends
           for j in range(i + 1, len(lines)):
              if lines[j][0] == ".":
                break
           if (j == len(lines) - 1 and lines[j][0] != "."): j+=1 
           ret += [parserLookup[line[1:]](lines[i:j])] 
    return ret