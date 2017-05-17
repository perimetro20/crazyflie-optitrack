import time
from crazy_mocap import CrazyMocap


if __name__ == '__main__':
    # Instantiate the CrazyMocap class
    cm = CrazyMocap()

    # Control loop
    while True:
        # Once the drone is connected send minimum power 
        if cm.connected:
            # Send roll, pitch, yaw, thrust
            cm.send_setpoint(0, 0, 0, 10001)
            # Print position, x, y and z according to the mocap
            print('Posicion:', cm.x, cm.y, cm.z)
            # Send the signal 100 times per second
            time.sleep(0.1)
