# forward declare types
from __future__ import annotations

from utils import uid

class PacketHeader:
    """
    A packet header will contain "meta-data" about the packet.
    This is data that your drone agent might not directly use, but is helpful to the underlying programs that provide packets to the drone agent.
    
    For example, the source_id help identify which drone sent out the packet, and therefore prevent a drone from reading its own packet. 
    """
    def __init__(self, source_id: str, id: str = "", ttl: int = 1):
        self.source_id: str = source_id
        """
        Stores the ID of the drone that dispatched this packet.
        """
        self.id: str = uid()
        """
        Store a unique identifier that can distinguish this packet from others.
        Helpful when packets persist in the communication fabric (using ttl) and a drone ID might have more than 1 packet associated with it.
        """
        """
        Time to Live. Decides how long the packet will last in the communication Fabric.

        ttl here does not work like IP
        what ttl will indicate is -> difference of current time - packet transmission or creation time
        but since in the simulation we don't really have the concept of "time", we will 
        specify a ttl that is decremented every simulation iteration
        """
        self.ttl: int = ttl

    def update(self):
        """
        Update is called every iteration.
        The only updates the header needs is that the ttl decrements by 1 every iteration.
        """
        self.ttl -= 1

    def __str__(self) -> str:
        return f"Source ID: {self.source_id}, Packet ID: {self.id}, TTL: {self.ttl}"

class Packet: 
    """
    Represents a Unit of Data a drone can send into the communication fabric.
    The user can decide its internal structure, there is no restriction.
    For debugging purposes, it helps to have the data as something that can be cast to a string using __str__

    Large packet sizes are not simulated, it is assumed the drone can transmit the entire packet into the communication fabric in one go.
    """
    def __init__(self, header: PacketHeader, data: any):
        self.header: PacketHeader = header
        """
        Header containing packet meta data.
        """
        self.data: any = data
        """
        Data of packet, doesn't have a type or structure.
        """

    def update(self):
        """
        Update is called every iteration.
        The only updates the packet needs is to update its header.
        """
        self.header.update()

    def __str__(self) -> str:
        return str(self.header) + "\n====================\n" + str(self.data)

class CommunicationFabric:
    """
    A simulation of the medium packets travel. 
    This abstracts the medium and protocol through which packets would travel.

    Drones dispatch packets into the fabric. Other drones fetch packets from the fabric. 
    """
    def __init__(self, buffer_size: int = 1):
        self.current_fabric: list[Packet] = []
        """
        Packets currently in the fabric.
        """
        self.buffer_size: int = buffer_size
        """
        Number of iterations the buffer can store the packet history for.
        """
        self.buffer: list[list[Packet]] = [] 
        """
        Stores a history of the packets in the fabric. 
        Mostly present to help debugging.

        While update will update the current_fabric, it will not update the packets in the buffer.
        """

    def update(self):
        """
        Update is called every iteration.
        This will push the current fabric state onto the buffer, and truncate the oldest fabric state if the buffer size is exceeded.
        This will also update every packet in the current_fabric. If packet TTLs drop below 1 it will remove the packet from the current_fabric.
        """
        new_fabric: list[Packet] = []
        for packet in self.current_fabric:
            if packet.header.ttl >= 1:
                new_fabric += [packet]
            packet.update()
        self.buffer += [self.current_fabric]
        self.buffer = self.buffer[:self.buffer_size]
        self.current_fabric = new_fabric

    def dispatch(self, packet: Packet):
        """
        This method will add packets into the fabric.
        """
        if (type(packet) != Packet):
            return
        self.current_fabric += [packet]

    def fetch(self, id: str) -> list[Packet]:
        """
        This method will return a list of packets that are appropriate for a drone with the given id.
        """
        return list(filter(lambda e: e.header.source_id != id and e.header.ttl >= 0, self.current_fabric))