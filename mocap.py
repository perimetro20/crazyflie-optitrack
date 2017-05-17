import logging
import sys
import cflib
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from NatNetClient import NatNetClient


logging.basicConfig(level=logging.ERROR)


class Mocap:
    """ Class for control of the drone, and position capturing
    
    This class initializes the connection with the drone, as well
    as with the MOCAP arena. It updates the current position of
    the drone, and allows for instructions to be sent to the
    CrazyFlie

    Variables
    ---------
    _cf: Crazyflie
    x: float
        The drone position in the x axis in meters (+(front)/-(back)
    y: float
        The drone position in the y axis in meters (height)
    z: float
        The drone position in the z axis in meters (+(right)/-(left))
    roll: float
    pitch: float
    yaw: float
    """

    def __init__(self):
        """ Initialize all the variables and processes.

        This function is ran when it is first instantiated.
        """

        # Setup global drone position variables
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

        # Create a new instance of a NatNet Client
        streamingClient = NatNetClient()
        # Create a listener for the Rigid Body Information
        streamingClient.newFrameListener = self.receiveNewFrame
        streamingClient.rigidBodyListener = self.receiveRigidBodyFrame
        # Connect to Client to the NatNet Server on a new thread
        streamingClient.run()


    def receiveNewFrame(self, frameNumber, markerSetCount,
                        unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                        labeledMarkerCount, latency, timecode, timecodeSub,
                        timestamp, isRecording, trackedModelsChanged):
        """ This function receives all the frame data from the MOCAP system.
    
        This function is required in roder to properly initialize the
        NatNet Client, it currently does nothing, other than get the frame
        date, that will later be passed on to the receive RigidBodyFrame.
        """
        pass


    def receiveRigidBodyFrame(self, id, position, rotation):
        """ Update the drone position variables from the MOCAP system.

        The drone position variables are updated automatically whenever a new
        Rigid Body Frame is received. This process happens automatically as
        the client is started on a separate thread and is always running.
        """
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.pitch = rotation[0]
        self.yaw = rotation[1]
        self.roll = rotation[2]
