import time
import sys
from crazy_mocap import CrazyMocap


if __name__ == '__main__':
    # Instantiate the CrazyMocap class
    cm = CrazyMocap()

    # Control loop
    while True:
        # Once the drone is connected send minimum power 
        if cm.connected:
            thrust_mult = 1
            thrust_step = 500
            thrust = 20000
            pitch = 0
            roll = 0
            yawrate = 0

            # Unlock startup thrust protection
            cm.send_setpoint(0, 0, 0, 0)

            while thrust >= 20000:
                cm.send_setpoint(roll, pitch, yawrate, thrust)
                time.sleep(0.1)
                if thrust >= 25000:
                    thrust_mult = -1
                thrust += thrust_step * thrust_mult
            cm.send_setpoint(0, 0, 0, 0)
            # Make sure that the last packet leaves before the link is closed
            # since the message queue is not flushed before closing
            time.sleep(0.1)
            break