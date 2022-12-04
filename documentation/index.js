URLS=[
"UTM/index.html",
"UTM/agents.html",
"UTM/aircell.html",
"UTM/comms.html",
"UTM/computed.html",
"UTM/constants.html",
"UTM/dispatcher.html",
"UTM/drone.html",
"UTM/loader.html",
"UTM/main.html",
"UTM/map.html",
"UTM/program.html",
"UTM/render_util.html",
"UTM/utils.html"
];
INDEX=[
{
"ref":"UTM",
"url":0,
"doc":""
},
{
"ref":"UTM.agents",
"url":1,
"doc":""
},
{
"ref":"UTM.agents.Agent",
"url":1,
"doc":"Taking in a state, the agent should return the action to be taken. Agent: entity in a program or environment capable of generating action. An agent uses perception of the environment to make decisions about actions to take. The perception capability is usually called a sensor. The actions can depend on the most recent perception or on the entire history (percept sequence). https: www.cs.iusb.edu/~danav/teach/c463/3_agents.html"
},
{
"ref":"UTM.agents.Agent.getAction",
"url":1,
"doc":"Given a state, return the appropriate action.",
"func":1
},
{
"ref":"UTM.agents.DroneAgent",
"url":1,
"doc":"Drone Agents will be used to control the drones. They will take a DroneState in as a state (this state is it's perception capability or it's sensor). Drone States will have memory where the history can be stored. env_context will represent the state of the environment that the drone has sensed."
},
{
"ref":"UTM.agents.DroneAgent.getAction",
"url":1,
"doc":"Given a state, return the appropriate action.",
"func":1
},
{
"ref":"UTM.agents.ForwardDroneAgent",
"url":1,
"doc":"A specialized agent that can only move forward. Not an ideal Agent, we want an intelligent one that can make decisions based on the contexts sensed. However this serves as a way to demonstrate how the Agent works since previous classes were abstract. Here the Agent just returns the Action as the current Drone Direction, therefore making the drone move forward. Ideally a drone will use the sensor data and depending on the state it will return an action (using conditionals and more advanced constructs)."
},
{
"ref":"UTM.agents.ForwardDroneAgent.getAction",
"url":1,
"doc":"Just return the direction the drone is going in, which is thought of as moving \"Forward\"",
"func":1
},
{
"ref":"UTM.aircell",
"url":2,
"doc":""
},
{
"ref":"UTM.aircell.Cell",
"url":2,
"doc":"Represents a single unit on the map. TODO: integrate with simulation."
},
{
"ref":"UTM.aircell.Cell.get_environment_potential",
"url":2,
"doc":"",
"func":1
},
{
"ref":"UTM.aircell.Cell.get_path_potential",
"url":2,
"doc":"",
"func":1
},
{
"ref":"UTM.aircell.Cell.rainfall",
"url":2,
"doc":"Represents rainfall in mm. TODO: check rainfall requirements (light rainfall should be okay with most drones)."
},
{
"ref":"UTM.aircell.Cell.temperature",
"url":2,
"doc":"Represents temperature in degrees C If it is not in the range 40F  60F"
},
{
"ref":"UTM.aircell.Cell.windspeed",
"url":2,
"doc":"Represents windspeed in TODO: check on windspeed that would affect drone (drone speed - 10 mph) TODO: check the windspeed is managed as a vector (for directionality)"
},
{
"ref":"UTM.aircell.AirCell",
"url":2,
"doc":"AirCells are the units on the map that a drone can occupy. TODO: complete and integrate with simulation. Follow up with Saanvi"
},
{
"ref":"UTM.aircell.AirCell.is_empty",
"url":2,
"doc":"",
"func":1
},
{
"ref":"UTM.aircell.AirCell.add_drone",
"url":2,
"doc":"",
"func":1
},
{
"ref":"UTM.aircell.AirCell.rainfall",
"url":2,
"doc":"Represents rainfall in mm. TODO: check rainfall requirements (light rainfall should be okay with most drones)."
},
{
"ref":"UTM.aircell.AirCell.temperature",
"url":2,
"doc":"Represents temperature in degrees C If it is not in the range 40F  60F"
},
{
"ref":"UTM.aircell.AirCell.windspeed",
"url":2,
"doc":"Represents windspeed in TODO: check on windspeed that would affect drone (drone speed - 10 mph) TODO: check the windspeed is managed as a vector (for directionality)"
},
{
"ref":"UTM.aircell.get_aircell_potential",
"url":2,
"doc":"This method is redundant, should be encapsulated in the right part of the simulation.",
"func":1
},
{
"ref":"UTM.comms",
"url":3,
"doc":""
},
{
"ref":"UTM.comms.PacketHeader",
"url":3,
"doc":"A packet header will contain \"meta-data\" about the packet. This is data that your drone agent might not directly use, but is helpful to the underlying programs that provide packets to the drone agent. For example, the source_id help identify which drone sent out the packet, and therefore prevent a drone from reading its own packet."
},
{
"ref":"UTM.comms.PacketHeader.update",
"url":3,
"doc":"Update is called every iteration. The only updates the header needs is that the ttl decrements by 1 every iteration.",
"func":1
},
{
"ref":"UTM.comms.PacketHeader.source_id",
"url":3,
"doc":"Stores the ID of the drone that dispatched this packet."
},
{
"ref":"UTM.comms.PacketHeader.id",
"url":3,
"doc":"Store a unique identifier that can distinguish this packet from others. Helpful when packets persist in the communication fabric (using ttl) and a drone ID might have more than 1 packet associated with it."
},
{
"ref":"UTM.comms.Packet",
"url":3,
"doc":"Represents a Unit of Data a drone can send into the communication fabric. The user can decide its internal structure, there is no restriction. For debugging purposes, it helps to have the data as something that can be cast to a string using __str__ Large packet sizes are not simulated, it is assumed the drone can transmit the entire packet into the communication fabric in one go."
},
{
"ref":"UTM.comms.Packet.update",
"url":3,
"doc":"Update is called every iteration. The only updates the packet needs is to update its header.",
"func":1
},
{
"ref":"UTM.comms.Packet.header",
"url":3,
"doc":"Header containing packet meta data."
},
{
"ref":"UTM.comms.Packet.data",
"url":3,
"doc":"Data of packet, doesn't have a type or structure."
},
{
"ref":"UTM.comms.CommunicationFabric",
"url":3,
"doc":"A simulation of the medium packets travel. This abstracts the medium and protocol through which packets would travel. Drones dispatch packets into the fabric. Other drones fetch packets from the fabric."
},
{
"ref":"UTM.comms.CommunicationFabric.update",
"url":3,
"doc":"Update is called every iteration. This will push the current fabric state onto the buffer, and truncate the oldest fabric state if the buffer size is exceeded. This will also update every packet in the current_fabric. If packet TTLs drop below 1 it will remove the packet from the current_fabric.",
"func":1
},
{
"ref":"UTM.comms.CommunicationFabric.dispatch",
"url":3,
"doc":"This method will add packets into the fabric.",
"func":1
},
{
"ref":"UTM.comms.CommunicationFabric.fetch",
"url":3,
"doc":"This method will return a list of packets that are appropriate for a drone with the given id.",
"func":1
},
{
"ref":"UTM.comms.CommunicationFabric.current_fabric",
"url":3,
"doc":"Packets currently in the fabric."
},
{
"ref":"UTM.comms.CommunicationFabric.buffer_size",
"url":3,
"doc":"Number of iterations the buffer can store the packet history for."
},
{
"ref":"UTM.comms.CommunicationFabric.buffer",
"url":3,
"doc":"Stores a history of the packets in the fabric. Mostly present to help debugging. While update will update the current_fabric, it will not update the packets in the buffer."
},
{
"ref":"UTM.computed",
"url":4,
"doc":""
},
{
"ref":"UTM.computed.alphaFromZ",
"url":4,
"doc":"",
"func":1
},
{
"ref":"UTM.constants",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.color_lookup",
"url":5,
"doc":"Dictionary mapping symbols to colors, useful for legacy textbased map."
},
{
"ref":"UTM.constants.priorityColorMap",
"url":5,
"doc":"Dictionary that will return the color of a drone based on it's priority. Replaced by priorityImageMap."
},
{
"ref":"UTM.constants.priorityImageMap",
"url":5,
"doc":"Dictionary that will return the image of a drone based on it's priority."
},
{
"ref":"UTM.constants.BLOCK_SIZE",
"url":5,
"doc":"Pixel size of 1 block"
},
{
"ref":"UTM.constants.MAX_ELEMENTS_IN_BLOCK",
"url":5,
"doc":"if there are more than 100 elements in a block, the highest ones are not visible generally, optimize the simulation to have not more than 4-5 elements a block"
},
{
"ref":"UTM.constants.Dimension2D",
"url":5,
"doc":"Represents 2 Dimensional measurements."
},
{
"ref":"UTM.constants.Dimension2D.width",
"url":5,
"doc":"Width Dimension."
},
{
"ref":"UTM.constants.Dimension2D.height",
"url":5,
"doc":"Height Dimension."
},
{
"ref":"UTM.constants.Point2D",
"url":5,
"doc":"Represents 2 Dimensional Coordinates."
},
{
"ref":"UTM.constants.Point2D.x",
"url":5,
"doc":"x coordinate."
},
{
"ref":"UTM.constants.Point2D.y",
"url":5,
"doc":"y coordinate."
},
{
"ref":"UTM.constants.Orientation2D",
"url":5,
"doc":"Represents 2 Dimensional Orientation. Only Supports Standard Orientations (Vertical and Horizontal)"
},
{
"ref":"UTM.constants.Orientation2D.HORIZONTAL",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.Orientation2D.VERTICAL",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.RNG",
"url":5,
"doc":"Random Number Generator (Pseudo). Uses built in random generator. Since that generator doesnt have a discrete class but does have a state, this class just stores the state of the rng. When a new instance is created with a seed, it saves the current state of random, sets random the a new generator with the seed, stores that new state in this class, and restors the current version."
},
{
"ref":"UTM.constants.RNG.randint",
"url":5,
"doc":"Functionally identical to random.randint() but with the seed for this instance without affecting the global random generator.",
"func":1
},
{
"ref":"UTM.constants.RNG.seed",
"url":5,
"doc":"seed of the rng"
},
{
"ref":"UTM.constants.RNG.rng",
"url":5,
"doc":"Stores the value of random.getstate() for this instance of the rng"
},
{
"ref":"UTM.constants.Action2D",
"url":5,
"doc":"Represents 2 Dimensional Actions. Semantically equal to 2 Dimensional Directions (there is no separate class)."
},
{
"ref":"UTM.constants.Action2D.to_vec",
"url":5,
"doc":"Converts an Action to a Vector that can be thought of as a normal direction vector.",
"func":1
},
{
"ref":"UTM.constants.Action2D.NORTH",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.Action2D.SOUTH",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.Action2D.EAST",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.Action2D.WEST",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.Action2D.NOP",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.Action2D.RIGHT",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.Action2D.LEFT",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.Action2D.REVERSE",
"url":5,
"doc":""
},
{
"ref":"UTM.constants.MovementVector2D",
"url":5,
"doc":"MovementVector2Ds will hold the position and the direction of the object TODO: Drone direction is it's next action. we assume for now that changing directions is instantaneous"
},
{
"ref":"UTM.constants.MovementVector2D.getCoords",
"url":5,
"doc":"Get a Point2D Object representing the coordinate of the object.",
"func":1
},
{
"ref":"UTM.constants.MovementVector2D.nextMovementVector",
"url":5,
"doc":"Sets the current Direction to the one provided, then updates the coordinates to move in that direction. Does not update in place, but returns a new MovementVector",
"func":1
},
{
"ref":"UTM.constants.MovementVector2D.x",
"url":5,
"doc":"x coordinate of the object."
},
{
"ref":"UTM.constants.MovementVector2D.y",
"url":5,
"doc":"y cooredinate of the object."
},
{
"ref":"UTM.constants.MovementVector2D.direction",
"url":5,
"doc":"Direction of the object."
},
{
"ref":"UTM.constants.DroneSimContext",
"url":5,
"doc":"Represents the Information that will be passed into the drone. Can be thought of its memory + its sensed data."
},
{
"ref":"UTM.constants.DroneSimContext.get_containing_corridor",
"url":5,
"doc":"Return the first corridor in the list that the x, y coordinates fall in.",
"func":1
},
{
"ref":"UTM.constants.DroneSimContext.get_containing_intersection",
"url":5,
"doc":"Return the first intersection in the list that the x, y coordinates fall in.",
"func":1
},
{
"ref":"UTM.constants.DroneSimContext.corridors",
"url":5,
"doc":"List of Corridors on the map."
},
{
"ref":"UTM.constants.DroneSimContext.intersections",
"url":5,
"doc":"List of intersections on the map."
},
{
"ref":"UTM.constants.DroneSimContext.comms_buffer",
"url":5,
"doc":"Packets received by the drone"
},
{
"ref":"UTM.constants.DroneSimContext.dispatch",
"url":5,
"doc":"Callable that the drone can use to dispatch packets into the Communication Fabric."
},
{
"ref":"UTM.dispatcher",
"url":6,
"doc":""
},
{
"ref":"UTM.dispatcher.BinaryProbabilityDistribution",
"url":6,
"doc":"A BinaryProbabilityDistribution is a class that will help generate a sequenece of boolean values of true and false."
},
{
"ref":"UTM.dispatcher.BinaryProbabilityDistribution.tick",
"url":6,
"doc":"Abstract: Every time this function is called, the generator will generate a new boolean value.",
"func":1
},
{
"ref":"UTM.dispatcher.BinaryPeriodicDistribution",
"url":6,
"doc":"A BinaryPeriodicDistribution will generate a single true over a period given a probability value. A seed can optionally be provieded to control the sequence generated."
},
{
"ref":"UTM.dispatcher.BinaryPeriodicDistribution.tick",
"url":6,
"doc":"If the difference in the iter and last_iter is greater than or equal to the period, it will attempt to generate a True with the given probability.",
"func":1
},
{
"ref":"UTM.dispatcher.BinaryPeriodicDistribution.update",
"url":6,
"doc":"Called to keep track of the number of iterations that have passed in the simulation to keep track of the period.",
"func":1
},
{
"ref":"UTM.dispatcher.BinaryPeriodicDistribution.period",
"url":6,
"doc":"The interval length for one true value."
},
{
"ref":"UTM.dispatcher.BinaryPeriodicDistribution.prob",
"url":6,
"doc":"The probability with which the true will be generated over that period."
},
{
"ref":"UTM.dispatcher.BinaryPeriodicDistribution.seed",
"url":6,
"doc":"The seed that this generator is based on."
},
{
"ref":"UTM.dispatcher.BinaryPeriodicDistribution.rng",
"url":6,
"doc":"The random number generator to generate a sequence of random numbers that will be converted to a boolean distribution."
},
{
"ref":"UTM.dispatcher.BinaryPeriodicDistribution.iter",
"url":6,
"doc":"Number of iterations that have passed (to keep track of the period)."
},
{
"ref":"UTM.dispatcher.BinaryPeriodicDistribution.last_iter",
"url":6,
"doc":"Number of iterations that have passed since last generation (to keep track of the period)."
},
{
"ref":"UTM.dispatcher.DispatchVertiport",
"url":6,
"doc":"Currently Dispatch Vertiports serve to provide a form of traffic generation. Given a coordinate, a priority and a direction, dispatch vertiports generate drones with those attributes. Dispatch Units are powered by DroneGenerators, that can have different probabilistic distributions powering them. The main working is, the unit will tick the generator every iteration, and if the tick returns true it will dispatch a drone on the map. TODO: add drone destination properties. TODO: look into -> joby aviation, Bell Labs"
},
{
"ref":"UTM.dispatcher.DispatchVertiport.dispatch",
"url":6,
"doc":"",
"func":1
},
{
"ref":"UTM.dispatcher.DispatchVertiport.render",
"url":6,
"doc":"",
"func":1
},
{
"ref":"UTM.dispatcher.DispatchVertiport.update",
"url":6,
"doc":"",
"func":1
},
{
"ref":"UTM.dispatcher.DispatchVertiport.x",
"url":6,
"doc":"x coordinate of the vertiport on the map."
},
{
"ref":"UTM.dispatcher.DispatchVertiport.y",
"url":6,
"doc":"y coordinate of the vertiport on the map."
},
{
"ref":"UTM.dispatcher.DispatchVertiport.dir",
"url":6,
"doc":"direction that the drones are spawned in."
},
{
"ref":"UTM.dispatcher.DispatchVertiport.priority",
"url":6,
"doc":"priority of the drones spawned in."
},
{
"ref":"UTM.dispatcher.DispatchVertiport.count",
"url":6,
"doc":"keeps track of how many drones are spawned by this vertiport."
},
{
"ref":"UTM.dispatcher.DispatchVertiport.generator",
"url":6,
"doc":"A DroneGenerator that has a probabilistic model to allow this dispatch unit to spawn drones."
},
{
"ref":"UTM.dispatcher.DispatchVertiport.name",
"url":6,
"doc":"Name of this dispatch unit."
},
{
"ref":"UTM.dispatcher.ReceiveVertiport",
"url":6,
"doc":"Receive vertiports are the opposite of dispatch vertiports, they will receive drones if the drone goal matches the receive vertiport. The drone goal can currently only be a receive vertiport's coordinates, or it can be out of bounds for the map to pick up once the drone goes offscreent."
},
{
"ref":"UTM.dispatcher.ReceiveVertiport.receive",
"url":6,
"doc":"Will gracefully shutdown the drone and then update its reference count, given that this vertiport was the drone's goal.",
"func":1
},
{
"ref":"UTM.dispatcher.ReceiveVertiport.has",
"url":6,
"doc":"Will check if the vertiport is at the given x and y coordinate.",
"func":1
},
{
"ref":"UTM.dispatcher.ReceiveVertiport.x",
"url":6,
"doc":"The x coordinate of the receive vertiport."
},
{
"ref":"UTM.dispatcher.ReceiveVertiport.y",
"url":6,
"doc":"The y coordinate of the receive vertiport."
},
{
"ref":"UTM.dispatcher.ReceiveVertiport.ref_count",
"url":6,
"doc":"The number of drones this vertiport has received."
},
{
"ref":"UTM.drone",
"url":7,
"doc":""
},
{
"ref":"UTM.drone.DroneType",
"url":7,
"doc":"Class to represent a type of drones. Will keep track of physical attributes of the drone. TODO: This will be useful with the AirCell class where the drone type will determine what weather the drone can fly through."
},
{
"ref":"UTM.drone.SmallDroneType",
"url":7,
"doc":"A small drone type, akin to  . TODO: Ask Saanvi"
},
{
"ref":"UTM.drone.DroneState",
"url":7,
"doc":"DroneStates hold the state of a drone (speed, priority) for the simulation. The program we write on the drone agent will not receive a DroneState, but a context of this state that will have copied values so a malicious program cannot modify the simulation"
},
{
"ref":"UTM.drone.DroneState.getCoords",
"url":7,
"doc":"Returns teh coordinates of the drone from its movement vector.",
"func":1
},
{
"ref":"UTM.drone.DroneState.getDirection",
"url":7,
"doc":"Returns the direction of the drone from its movement vector.",
"func":1
},
{
"ref":"UTM.drone.DroneState.applyAction",
"url":7,
"doc":"Applies the given action to the drone, updating it's movement vector.",
"func":1
},
{
"ref":"UTM.drone.DroneState.render",
"url":7,
"doc":"Renders the drone onto the screen.",
"func":1
},
{
"ref":"UTM.drone.DroneState.shutdown",
"url":7,
"doc":"Gracefully shuts down the drone.",
"func":1
},
{
"ref":"UTM.drone.DroneState.id",
"url":7,
"doc":"A unique identifier representing the drone."
},
{
"ref":"UTM.drone.DroneState.name",
"url":7,
"doc":"A name for the drone. This is not unique"
},
{
"ref":"UTM.drone.DroneState.priority",
"url":7,
"doc":"The priority of the drone. Lower numbers mean higher priority."
},
{
"ref":"UTM.drone.DroneState.movement_vector",
"url":7,
"doc":"Movement vector representing the current movement of the drone."
},
{
"ref":"UTM.drone.DroneState.inital_vector",
"url":7,
"doc":"Movement vector representing the initial state of the drone."
},
{
"ref":"UTM.drone.DroneState.goal",
"url":7,
"doc":"Coordinate representing the final destination of the Drone. When this is None, it will be assumed that the drone is trying to exit the Map Area."
},
{
"ref":"UTM.drone.MemoryContext",
"url":7,
"doc":"A class to hold the memory of a drone. Basically a dictionary for the time being. Store data in a key-value fashion."
},
{
"ref":"UTM.drone.DroneStateContext",
"url":7,
"doc":"A class to pass a drone state from the simulation into the program. This class exists to prevent a user from directly interacting with the simulation. Contains a copy of the simulation DroneState with only those attributes and behaviours that are required by the User program."
},
{
"ref":"UTM.drone.DroneStateContext.id",
"url":7,
"doc":"A unique identifier representing the drone."
},
{
"ref":"UTM.drone.DroneStateContext.name",
"url":7,
"doc":"A name for the drone. This is not unique"
},
{
"ref":"UTM.drone.DroneStateContext.priority",
"url":7,
"doc":"The priority of the drone. Lower numbers mean higher priority."
},
{
"ref":"UTM.drone.DroneStateContext.x",
"url":7,
"doc":"Current x coordinate of the drone."
},
{
"ref":"UTM.drone.DroneStateContext.y",
"url":7,
"doc":"Current y coordinate of the drone."
},
{
"ref":"UTM.drone.DroneStateContext.dir",
"url":7,
"doc":"Current direction of the drone."
},
{
"ref":"UTM.drone.DroneStateContext.init_x",
"url":7,
"doc":"Initial x coordinate of the drone"
},
{
"ref":"UTM.drone.DroneStateContext.init_y",
"url":7,
"doc":"Initial y coordinate of the drone"
},
{
"ref":"UTM.drone.DroneStateContext.init_dir",
"url":7,
"doc":"Initial direction of the drone"
},
{
"ref":"UTM.drone.DroneStateContext.goal_x",
"url":7,
"doc":"x coordinate of Goal of the drone"
},
{
"ref":"UTM.drone.DroneStateContext.goal_y",
"url":7,
"doc":"y coordinate of Goal of the drone"
},
{
"ref":"UTM.drone.DroneStateContext.mem",
"url":7,
"doc":"The memory context belonging to this drone."
},
{
"ref":"UTM.loader",
"url":8,
"doc":""
},
{
"ref":"UTM.loader.tokenize",
"url":8,
"doc":"",
"func":1
},
{
"ref":"UTM.loader.loadMaps",
"url":8,
"doc":"",
"func":1
},
{
"ref":"UTM.main",
"url":9,
"doc":""
},
{
"ref":"UTM.main.SimulationController",
"url":9,
"doc":""
},
{
"ref":"UTM.main.render",
"url":9,
"doc":"",
"func":1
},
{
"ref":"UTM.main.input",
"url":9,
"doc":"",
"func":1
},
{
"ref":"UTM.main.update",
"url":9,
"doc":"",
"func":1
},
{
"ref":"UTM.main.cleanup",
"url":9,
"doc":"",
"func":1
},
{
"ref":"UTM.main.verify",
"url":9,
"doc":"",
"func":1
},
{
"ref":"UTM.main.run",
"url":9,
"doc":"",
"func":1
},
{
"ref":"UTM.map",
"url":10,
"doc":""
},
{
"ref":"UTM.map.Channel2D",
"url":10,
"doc":"Class representing an individual channel in a 2D map. A channel is a line of air cells. The channels currently are unidirectional. Multiple channels make an aircorridor."
},
{
"ref":"UTM.map.Channel2D.getDirection",
"url":10,
"doc":"Returns the direction of the channel. Drones must flow along this direction unless in intersections.",
"func":1
},
{
"ref":"UTM.map.Channel2D.idx",
"url":10,
"doc":"The index of the channel in the corridor."
},
{
"ref":"UTM.map.Channel2D.dir",
"url":10,
"doc":"The direction of the channel. Determines which directions the drones can move."
},
{
"ref":"UTM.map.Channel2D.orientation",
"url":10,
"doc":"The orientation of the channel on the map. Vertical or Horizontal."
},
{
"ref":"UTM.map.Corridor2D",
"url":10,
"doc":"A class representing a Corridor in a 2D Map. Contains multiple channels. Drones can only be in one channel at a time unless in an intersection. If a Corridor is added into a map file as: CORRIDOR H 0 9 20 2 1 Corridor direction is Horizontal. Corridor start coordinate is (0, 9). Corridor length is 20. Corridor has 2 channels. The direction value is 1. Since there are 2 corridors, we will convert this into a 2 digit binary number: 01 Since this is a horizontal corridor, channels can only have EAST or WEST directions. Channel at index 0 will have direction associated with 0 () and channel at index 1 will have direction associated with 1 ()."
},
{
"ref":"UTM.map.Corridor2D.getRectangle",
"url":10,
"doc":"returns the rectangle containing the entire corridor.",
"func":1
},
{
"ref":"UTM.map.Corridor2D.intersects",
"url":10,
"doc":"checks if 2 corridors intersect.",
"func":1
},
{
"ref":"UTM.map.Corridor2D.getIntersectionBounds",
"url":10,
"doc":"returns the rectangle representing the intersection of 2 corridors.",
"func":1
},
{
"ref":"UTM.map.Corridor2D.render",
"url":10,
"doc":"Draws the corridor onto the screen.",
"func":1
},
{
"ref":"UTM.map.Corridor2D.has",
"url":10,
"doc":"Checks that the given coordinates are inside the corridor.",
"func":1
},
{
"ref":"UTM.map.Corridor2D.get_containing_channel",
"url":10,
"doc":"returns the channel containing the given coordinate.",
"func":1
},
{
"ref":"UTM.map.Corridor2D.orientation",
"url":10,
"doc":"Represents the orientation of the corridor."
},
{
"ref":"UTM.map.Corridor2D.x",
"url":10,
"doc":"The x coordinate of the top left point of the corridor."
},
{
"ref":"UTM.map.Corridor2D.y",
"url":10,
"doc":"The y coordinate of the top left point of the corridor."
},
{
"ref":"UTM.map.Corridor2D.length",
"url":10,
"doc":"The length of the corridor."
},
{
"ref":"UTM.map.Corridor2D.width",
"url":10,
"doc":"The width of the corridor."
},
{
"ref":"UTM.map.Corridor2D.channels",
"url":10,
"doc":"A list of all the channels in the corridor."
},
{
"ref":"UTM.map.Intersection",
"url":10,
"doc":"A class representing an intersection in 2D."
},
{
"ref":"UTM.map.Intersection.has",
"url":10,
"doc":"Checks if an intersection contains the given x, y coordinates.",
"func":1
},
{
"ref":"UTM.map.Intersection.render",
"url":10,
"doc":"Draws the intersection on the map.",
"func":1
},
{
"ref":"UTM.map.Intersection.corridor1",
"url":10,
"doc":"The first corridor this intersection is a part of."
},
{
"ref":"UTM.map.Intersection.corridor2",
"url":10,
"doc":"The second corridor this intersection is a part of."
},
{
"ref":"UTM.map.Map2D",
"url":10,
"doc":"A class representing a 2D Map. TODO: 2 ways of keeping track of a map: sparse and aircell. Currently Sparse implemented."
},
{
"ref":"UTM.map.Map2D.has",
"url":10,
"doc":"checks if this given x, y coordinate is in the map bounds.",
"func":1
},
{
"ref":"UTM.map.Map2D.get_containing_corridor",
"url":10,
"doc":"given an x, y coordinate, returns the corridor that would contain this coordinate or else returns None.",
"func":1
},
{
"ref":"UTM.map.Map2D.get_containing_intersection",
"url":10,
"doc":"given an x, y coordinate, returns the intersection that would contain this coordinate or else returns None.",
"func":1
},
{
"ref":"UTM.map.Map2D.update_intersections",
"url":10,
"doc":"Called to compute all the intersections on the map given the corridors on this map.",
"func":1
},
{
"ref":"UTM.map.Map2D.to_arr",
"url":10,
"doc":"Converts the map to an array representation. TODO: describe representation.",
"func":1
},
{
"ref":"UTM.map.Map2D.render",
"url":10,
"doc":"Draws the map onto the screen.",
"func":1
},
{
"ref":"UTM.map.Map2D.update",
"url":10,
"doc":"Updates all the components on the map.",
"func":1
},
{
"ref":"UTM.map.Map2D.set_global_agent",
"url":10,
"doc":"Changes the Agents controlling each drone on the simulation.",
"func":1
},
{
"ref":"UTM.map.Map2D.apply_simulation_settings",
"url":10,
"doc":"Applies the given settings onto the simulation. TODO: describe the settings dict.",
"func":1
},
{
"ref":"UTM.map.Map2D.shutdown",
"url":10,
"doc":"Shuts down the drone and removes it from the map (if not called here it will still be on the map and will be an error). Furthermore there might be a mem leak.",
"func":1
},
{
"ref":"UTM.map.Map2D.corridors",
"url":10,
"doc":"A list of all corridors in this map."
},
{
"ref":"UTM.map.Map2D.dimension",
"url":10,
"doc":"The Dimensions of this map."
},
{
"ref":"UTM.map.Map2D.intersections",
"url":10,
"doc":"A list of all the intersections of the map."
},
{
"ref":"UTM.map.Map2D.drones_states",
"url":10,
"doc":"A list of all the drone states present on the map."
},
{
"ref":"UTM.map.Map2D.agent",
"url":10,
"doc":"The agent controlling the drone states on the map."
},
{
"ref":"UTM.map.Map2D.dispatchers",
"url":10,
"doc":"A list of all the dispatcher vertiports in the map."
},
{
"ref":"UTM.map.Map2D.goals",
"url":10,
"doc":"A dictionary mapping all receiving vertiports to all drones that have that vertiport's coordinates as a goal."
},
{
"ref":"UTM.map.Map2D.comms",
"url":10,
"doc":"The communication fabric on this map."
},
{
"ref":"UTM.map.Map2D.mems",
"url":10,
"doc":"The memory of all drones on this map. TODO: encapsulate in drone state"
},
{
"ref":"UTM.program",
"url":11,
"doc":""
},
{
"ref":"UTM.program.CommunicationCapableAgent",
"url":11,
"doc":"A simple agent to show how Drone communication will work using the dispatch/ fetch (push/ pull) mechanism. Fetching is done outside the agent, assumed to be an abstraction of the drone's communication drivers. env_context has a comms_buffer that will contain all Packet instances relevant to this drone. At the moment, if a packet has a drone_id different from the Drone the Agent is working on, it is relevant to the current Drone. However, in later versions of the simulation, there should be a feature to modify which packet the driver can pick up and allow the drone to fetch for the agent.  TODO"
},
{
"ref":"UTM.program.CommunicationCapableAgent.getAction",
"url":11,
"doc":"Given a state, return the appropriate action.",
"func":1
},
{
"ref":"UTM.program.TurnRightAtIntersectionAgent",
"url":11,
"doc":"A simple agent that is slightly more advanced than the inbuilt ForwardDroneAgent. This one will detect when we are in an intersection and automatically move right. Please use maps/intersection-right.map with this agent to prevent crashes due to drones not reaching the goal. When we enter the intersection, we will need to just turn right."
},
{
"ref":"UTM.program.TurnRightAtIntersectionAgent.getAction",
"url":11,
"doc":"Given a state, return the appropriate action.",
"func":1
},
{
"ref":"UTM.program.TurnLeftAtIntersectionAgent",
"url":11,
"doc":"A complex agent that is slightly more advanced than the TurnRightAtIntersectionAgent. This one will detect when we are in an intersection and automatically move left. Please use maps/intersection-left.map with this agent to prevent crashes due to drones not reaching the goal. In the map, to turn left at the intersection, our drone needs to make sure that it comes out on the correct channel. If we are going in from the \"Bottom\" \"East\" Channel, the drone must come out through the \"Right\" \"North\" Channel. | X | ^ | Drone -> | > | ^ | This is because immediately turning left into an intersection will result in: | ^ | X | Drone -> | ^ | X | however, we now see that the drone is moving North along a South Channel. This will be illegal in the simulation. This means that it must make a long turn at the intersection, which needs to be done in 3 iterations: To achieve this functionality, we will be using the memory the simulation provides each Drone. We can do this by mimicing a state machine to keep track of where we are in the intersection. I have simplified the intesection to use a list keeping track of whether we were in an intersection in the last 3 simulation states. If the last 2 simulation states were in an intersection, we turn left. Otherwise we move forward. This forces a long turn."
},
{
"ref":"UTM.program.TurnLeftAtIntersectionAgent.getAction",
"url":11,
"doc":"Given a state, return the appropriate action.",
"func":1
},
{
"ref":"UTM.program.DFSAgent",
"url":11,
"doc":"TODO: basic DFS implementation to show how to check legality of steps and perform known algos TODO: demonstrate that storing data at the agent level is a mem leak -> will never get cleared."
},
{
"ref":"UTM.program.DFSAgent.getAction",
"url":11,
"doc":"Given a state, return the appropriate action.",
"func":1
},
{
"ref":"UTM.program.BFSAgent",
"url":11,
"doc":"TODO: ask ananay for description, since it has not been put on the github rn."
},
{
"ref":"UTM.program.BFSAgent.getAction",
"url":11,
"doc":"Given a state, return the appropriate action.",
"func":1
},
{
"ref":"UTM.program.AStarAgent",
"url":11,
"doc":"TODO: ask ananay for description, since it has not been put on the github rn."
},
{
"ref":"UTM.program.AStarAgent.getAction",
"url":11,
"doc":"Given a state, return the appropriate action.",
"func":1
},
{
"ref":"UTM.program.DjikstrasAgent",
"url":11,
"doc":"TODO: ask ananay for description, since it has not been put on the github rn."
},
{
"ref":"UTM.program.DjikstrasAgent.getAction",
"url":11,
"doc":"Given a state, return the appropriate action.",
"func":1
},
{
"ref":"UTM.render_util",
"url":12,
"doc":""
},
{
"ref":"UTM.render_util.drawAlphaRect",
"url":12,
"doc":"",
"func":1
},
{
"ref":"UTM.render_util.drawAlphaCoordBlock",
"url":12,
"doc":"",
"func":1
},
{
"ref":"UTM.render_util.drawCoordBlock",
"url":12,
"doc":"",
"func":1
},
{
"ref":"UTM.render_util.drawDroneIcon",
"url":12,
"doc":"",
"func":1
},
{
"ref":"UTM.render_util.drawArrow",
"url":12,
"doc":"",
"func":1
},
{
"ref":"UTM.utils",
"url":13,
"doc":""
},
{
"ref":"UTM.utils.getBlockSize",
"url":13,
"doc":"",
"func":1
},
{
"ref":"UTM.utils.blockPositiontoGridIndex",
"url":13,
"doc":"",
"func":1
},
{
"ref":"UTM.utils.polToCart",
"url":13,
"doc":"",
"func":1
},
{
"ref":"UTM.utils.has",
"url":13,
"doc":"",
"func":1
},
{
"ref":"UTM.utils.uid",
"url":13,
"doc":"",
"func":1
}
]