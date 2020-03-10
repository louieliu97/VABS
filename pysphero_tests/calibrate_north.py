from pysphero.core import Sphero
from pysphero.driving import Direction, DirectionRawMotor
from time import sleep
from typing import Dict
from pysphero.device_api.sensor import CoreTime, Accelerometer, Gyroscope, Velocity
from pysphero.device_api.user_io import Color


def main():
    #mac_address = "F1:B6:E8:5A:7B:D7"  # Sphero 1
    mac_address = "F1:8D:AE:17:9D:75" #Sphero 2
    with Sphero(mac_address=mac_address) as sphero:
        sphero.power.wake()
        sphero.sensor.magnetometer_calibrate_to_north()
        sleep(2)
        sphero.driving.drive_with_heading(speed=0, heading=0, direction=Direction.forward)
        sleep(1)
        #sphero.driving.reset_yaw()
        #sphero.driving.drive_with_heading(speed=100, heading=0, direction=Direction.forward)
        


if __name__ == "__main__":
    print("Calling main")
    main()
    print("Done")
