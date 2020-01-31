from pysphero.core import Sphero
from pysphero.driving import Direction, DirectionRawMotor
from time import sleep
from typing import Dict
from pysphero.device_api.sensor import CoreTime, Accelerometer, Gyroscope, Velocity
from pysphero.device_api.user_io import Color

accel = []
velo = []


def velocity_callback(data: Dict):
    info = ",".join("{:1.2f}".format(data.get(param)) for param in Velocity)
    print(f"[{data.get(CoreTime.core_time):1.2f}] Velocity (x,y): {info}")
    print("=" * 60)

    velo.append(info)

def notify_callback(data: Dict):
    info = ", ".join("{:1.2f}".format(data.get(param)) for param in Accelerometer)
    print(f"[{data.get(CoreTime.core_time):1.2f}] Accelerometer (x, y, z): {info}")
    print("=" * 60)
    #accel_old = accel[-1][1]
    accel.append(info)
    #accel_new = accel[-1][1]

    #if accel_new<accel_old:
     #   collison = True



def main():
    #mac_address = "F1:B6:E8:5A:7B:D7"  # Sphero 1
    mac_address = "F1:8D:AE:17:9D:75" #Sphero 2
    with Sphero(mac_address=mac_address) as sphero:
        sphero.power.wake()

        #print(f"Calibrating to North!")
        #sphero.sensor.magnetometer_calibrate_to_north()
        #sleep(5)
        #sphero.driving.drive_with_heading(0, 315, Direction.forward)

        print(f"Turning on Lights!")
        sphero.user_io.set_all_leds_8_bit_mask(front_color=Color(red=0xff), back_color=Color(blue=0xff))
        sphero.user_io.set_led_matrix_single_character("!", Color(red=0xff))
        # sphero.user_io.set_all_leds_8_bit_mask(front_color=Color(red=0xff))
        
        
        print(f"Resetting Yaw!")
        sphero.driving.reset_yaw()

        print(f"Sensors On!")
        sphero.sensor.set_notify(velocity_callback, CoreTime, Velocity)

        speed = 255
        heading = 0

        print(f"Motors Engaged!")
        #collision = False
        sphero.driving.drive_with_heading(speed, heading, Direction.forward)
        #sleep(0.5)
        print("Entering While Loop")
        #while not collision:
        while True:
            print("While Loop")
            sleep(0.25)
            if len(velo) >= 3:
                curr = velo[-1].split(',')
                prev = velo[-2].split(",")
                curr = [float(c) for c in curr]
                prev = [float(p) for p in prev]

                if abs(curr[1]) < abs(prev[1]):
                    #collision = True
                    #sphero.power.enter_soft_sleep()
                    #sphero.driving.set_stabilization()
                    sphero.driving.raw_motor(0, DirectionRawMotor.disable, 0, DirectionRawMotor.disable)
                    print("Collision detected, sleeping")
                    sphero.user_io.set_led_matrix_single_character("X", Color(red=0xff))
                    print(prev[1])
                    print(curr[1])
                    #sleep(0.5)
                    #sphero.driving.drive_with_heading(speed=0, heading=315, direction=Direction.forward)
                    break

       # sleep(0.5)
        print(f"Sensors Disengaged!")
        sphero.sensor.cancel_notify_sensors()

        sphero.driving.drive_with_heading(speed=0, heading=315, direction=Direction.forward)
       #print(f"Accelerometer data:{accel}")


if __name__ == "__main__":
    print("Calling main")
    main()
    print("Done")
