##################################################################################
# Title: camera.py
# Author: Kian Rossitto and Louie Liu
# Date: 15 April 2020
##################################################################################


from time import sleep
from typing import Dict

from pysphero.core import Sphero
from pysphero.driving import Direction
from pysphero.device_api.sensor import CoreTime, Accelerometer

def notify_callback(data: Dict):
    info = ", ".join("{:1.2f}".format(data.get(param)) for param in Accelerometer)
    print(f"[{data.get(CoreTime.core_time):1.2f}] Accelerometer (x, y, z): {info}")
    print("=" * 60)

def main():
    mac_address = "F1:B6:E8:5A:7B:D7" #Sphero 1
    #mac_address = "F1:8D:AE:17:9D:75" #Sphero 2
    with Sphero(mac_address=mac_address) as sphero:
        sphero.power.wake()
        sphero.sensor.set_notify(notify_callback, CoreTime, Accelerometer)
        print(f"Sensors On!")
        speed = 255
        heading = 0
        #sphero.driving.reset_yaw()
        sleep(1)
        sphero.driving.drive_with_heading(speed, heading, Direction.forward)
        print(f"Motors Engaged!")
        sleep(1)
        sphero.sensor.cancel_notify_sensors()
        print(f"Sensors Disengaged!")
        #a,b,c = sphero.sensor.get_sensor_streaming_mask()
        #print(a)
        #print(b)
        #print(c)


if __name__ == "__main__":
    print("Calling main")
    main()
    print("Done")
