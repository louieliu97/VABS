from pysphero_tests.pysphero.core import Sphero, SpheroCore
from pysphero_tests.pysphero.driving import Direction, DirectionRawMotor
from time import sleep
from typing import Dict
from pysphero_tests.pysphero.device_api.sensor import CoreTime, Accelerometer, Gyroscope, Velocity
from pysphero_tests.pysphero.device_api.user_io import Color, UserIOCommand, UserIO

class Cueball:
    def __init__(self):
        # mac_address = "F1:B6:E8:5A:7B:D7"  # Sphero 1
        mac_address = "F1:8D:AE:17:9D:75"  # Sphero 2
        self.sphero = Sphero(mac_address)
        self.sphero.__enter__()
        accel=[]
        velo=[]

    def velocity_callback(data: Dict):
        info = ",".join("{:1.2f}".format(data.get(param)) for param in Velocity)
        print(f"[{data.get(CoreTime.core_time):1.2f}] Velocity (x,y): {info}")
        print("=" * 60)

        velo.append(info)

    def notify_callback(data: Dict):
        info = ", ".join("{:1.2f}".format(data.get(param)) for param in Accelerometer)
        print(f"[{data.get(CoreTime.core_time):1.2f}] Accelerometer (x, y, z): {info}")
        print("=" * 60)
        # accel_old = accel[-1][1]
        accel.append(info)
        # accel_new = accel[-1][1]

        # if accel_new<accel_old:
        #   collison = True

    def rotate_cue (self, angle):
        """
        This function rotates the Sphero in place to a specified heading/angle

        @params: int angle (0-360)

        @returns none
        """

        #This part turns on the Red LED in Front and Blue LED in Back along with an arrow in the direction of rotation
        print(f"Turning on Lights!")
        self.sphero.user_io.set_all_leds_8_bit_mask(front_color=Color(red=0xff), back_color=Color(blue=0xff))
        self.sphero.user_io.set_led_matrix_single_character(">", Color(red=0xff))
        # sphero.user_io.set_all_leds_8_bit_mask(front_color=Color(red=0xff))

        #This resets the yaw so that heading of 0 degrees is straight ahead.
        print(f"Resetting Yaw!")
        self.sphero.driving.reset_yaw()

        #This rotates the sphero
        self.sphero.driving.drive_with_heading(speed=0, heading=angle)
        sleep(1)

    def drive_until_collison (self, speed):
        """
        This function makes the Sphero go straight ahead at a specified speed.
        Sphero will stop when it collides with something.

        @params: int speed (0-255)

        @returns none
        """
        self.sphero.power.wake()

        # print(f"Calibrating to North!")
        # sphero.sensor.magnetometer_calibrate_to_north()
        # sleep(5)
        # sphero.driving.drive_with_heading(0, 315, Direction.forward)

        print(f"Turning on Lights!")
        self.sphero.user_io.set_all_leds_8_bit_mask(front_color=Color(red=0xff), back_color=Color(blue=0xff))
        self.sphero.user_io.set_led_matrix_single_character("!", Color(red=0xff))
        # sphero.user_io.set_all_leds_8_bit_mask(front_color=Color(red=0xff))

        print(f"Resetting Yaw!")
        self.sphero.driving.reset_yaw()

        print(f"Sensors On!")
        self.sphero.sensor.set_notify(velocity_callback, CoreTime, Velocity)

        print(f"Motors Engaged!")
        # collision = False
        self.sphero.driving.drive_with_heading(speed, 0, Direction.forward)
        # sleep(0.5)
        print("Entering While Loop")
        # while not collision:
        while True:
            print("While Loop")
            sleep(0.25)
            if len(velo) >= 3:
                curr = velo[-1].split(',')
                prev = velo[-2].split(",")
                curr = [float(c) for c in curr]
                prev = [float(p) for p in prev]

                if abs(curr[1]) < abs(prev[1]):
                    # collision = True
                    # sphero.power.enter_soft_sleep()
                    # sphero.driving.set_stabilization()
                    self.sphero.driving.raw_motor(0, DirectionRawMotor.disable, 0, DirectionRawMotor.disable)
                    print("Collision detected, sleeping")
                    self.sphero.user_io.set_led_matrix_single_character("X", Color(red=0xff))
                    print(prev[1])
                    print(curr[1])
                    # sleep(0.5)
                    # sphero.driving.drive_with_heading(speed=0, heading=315, direction=Direction.forward)
                    break

        # sleep(0.5)
        print(f"Sensors Disengaged!")
        self.sphero.sensor.cancel_notify_sensors()

if __name__ == '__main__':
    z=Cueball()
    z.rotate_cue(180)

