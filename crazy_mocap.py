import logging
import sys
import cflib
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from NatNetClient import NatNetClient


logging.basicConfig(level=logging.ERROR)


class CrazyMocap:
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

        # No connection has been established yet
        self.connected = False

        # Initialize the low-level drivers (don't list the debug drivers)
        cflib.crtp.init_drivers(enable_debug_driver=False)
        # Scan for Crazyflies and use the first one found
        print('Scanning interfaces for Crazyflies...')
        available = cflib.crtp.scan_interfaces()
        print('Crazyflies found:')

        for i in available:
            print(i[0])

        if len(available) == 0:
            print('No Crazyflies found, cannot instantiate the class.')
            sys.exit()

        # Select the drone that we are going to connect to
        link_uri = available[0][0]
        self._cf = Crazyflie()

        # Add all the necessary callbacks for connection update status
        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        # Open link with the first drone found
        self._cf.open_link(link_uri)
        print('Connecting to %s' % link_uri)

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


    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded.
        """
        self.connected = True
        print('Connected')


    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)
        """
        self.connected = False
        print('Connection to %s failed: %s' % (link_uri, msg))


    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)
        """
        self.connected = False
        print('Connection to %s lost: %s' % (link_uri, msg))


    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)
        """
        self.connected = False
        print('Disconnected from %s' % link_uri)
        sys.exit()


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

    def send_setpoint(self, roll, pitch, yaw, thrust_power):
        """ Send an instruction to the drone so it can be manipulated

        arguments:
        roll: float
        pitch: float
        yaw: float
        thrust_power: int
            The range for this value is between 10000 and 60000
        """
        self._cf.commander.send_setpoint(roll, pitch, yaw, thrust_power)

