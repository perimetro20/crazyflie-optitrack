import time
import sys
from mocap import Mocap


if __name__ == '__main__':
    # Instantiate the CrazyMocap class
    cm = Mocap()
    cont = 0
    # Record position for 5 seconds and send it to a file
    print('Start tracking')
    start_time = time.time()
    # Select a file to store the info
    file = open('tracking_info.csv', 'w')
    # Write the headers to the file
    file.write('timestamp, x, y, z\n')
    while time.time() - start_time <= 5:
        # Get string to write
        data = '{}, {}, {}, {}\n'.format(int((time.time() - start_time) * 1000), cm.x, cm.y, cm.z)
        # Write to file timestamp (miliseconds sinc start), x, y and z according to the mocap to the file
        file.write(data)
        # Wait for one milisecond
        time.sleep(0.001)

    # Notify of finished 
    print('Finish')
