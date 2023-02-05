# Ultimate Question
Will there be an accident?
# Points to Note

1. There exists a ground control that works as a Database
   1. Weather Data is centralized
   2. High Level Decisions

## TODO

1. Make the Event,Delegate pattern work in python
2. Make a Cell Object

## Metrics

1. Traffic Rate
2. Drone Velocity
3. Minimum Distance between Drone
4. Traffic Density: How many total vehicles are there in the airspace in a given area.
5. Weather Monitoring: Quantifiable

## KPI
1. Total Time to Travel: How much time it took for a vehicle to travel from the starting point to its destination?
2. Intersection Delay: How long does the drone wait at an intersection?
3. Total Delay: Drones waiting for other drones (2 space gap etc.)
4. Base Time to Travel: How much time it will take to get to its end point without any other drones present.
5. Weather Delay: need to define (think about how you are injecting weather, UVR - UAV Volume restriction, depends on number of cells needed to reroute)

## Cell Class

1. Occupied: Boolean
2. Weather: Maybe a seperate Data Structure

## Paper Structure

Introduction - problem description
Lit Review - Introduce the acronyms, what other people are doing
Model - What have you done with regards to the problem statement
Experiments & Results - Proving the model is right
