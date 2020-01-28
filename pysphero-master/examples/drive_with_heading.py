import random
from time import sleep

from pysphero.core import Sphero
from pysphero.driving import Direction


def main():
    mac_address = "F1:B6:E8:5A:7B:D7" #Sphero 1
    #mac_address = "F1:8D:AE:17:9D:75" #Sphero 2
    with Sphero(mac_address=mac_address) as sphero:
        sphero.power.wake()

        for _ in range(5):
            sleep(2)
            speed = random.randint(50, 100)
            heading = random.randint(0, 360)
            print(f"Send drive with speed {speed} and heading {heading}")
            A,B,C = sphero.sensor.get_sensor_streaming_mask()
            print(f"A:{A}")
            print(f"B:{B}")
            print(f"C:{C}")

            sphero.driving.drive_with_heading(speed, heading, Direction.forward)
            print(f"A:{A}")
            print(f"B:{B}")
            print(f"C:{C}")


        sphero.power.enter_soft_sleep()


if __name__ == "__main__":
    main()
