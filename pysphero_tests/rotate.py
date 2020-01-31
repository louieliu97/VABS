from pysphero.core import Sphero
from pysphero.driving import Direction, DirectionRawMotor
from time import sleep
from typing import Dict
from pysphero.device_api.sensor import CoreTime, Accelerometer, Gyroscope, Velocity
from pysphero.device_api.user_io import Color


def main():
    mac_address = "F1:B6:E8:5A:7B:D7"  # Sphero 1
    # mac_address = "F1:8D:AE:17:9D:75" #Sphero 2
    with Sphero(mac_address=mac_address) as sphero:
        sphero.power.wake()


        print(f"Turning on Lights!")
        sphero.user_io.set_all_leds_8_bit_mask(front_color=Color(red=0xff), back_color=Color(blue=0xff))
        sphero.user_io.set_led_matrix_single_character(">", Color(red=0xff))
        # sphero.user_io.set_all_leds_8_bit_mask(front_color=Color(red=0xff))

        print(f"Resetting Yaw!")
        sphero.driving.reset_yaw()

        sphero.driving.drive_with_heading(speed=0,heading=180)
        sleep(1)





if __name__ == "__main__":
    print("Calling main")
    main()
    print("Done")
