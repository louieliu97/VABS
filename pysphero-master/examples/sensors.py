from time import sleep
from typing import Dict

from pysphero.core import Sphero
from pysphero.device_api.sensor import CoreTime, Quaternion


def notify_callback(data: Dict):
    info = ", ".join("{:1.2f}".format(data.get(param)) for param in Quaternion)
    print(f"[{data.get(CoreTime.core_time):1.2f}] Quaternion (x, y, z, w): {info}")
    print("=" * 60)


def main():
    mac_address = "F1:B6:E8:5A:7B:D7" #Sphero 1
    #mac_address = "F1:8D:AE:17:9D:75" #Sphero 2
    with Sphero(mac_address=mac_address) as sphero:
        sphero.power.wake()
        sphero.sensor.set_notify(notify_callback, CoreTime, Quaternion)
        sleep(2)
        sphero.sensor.cancel_notify_sensors()
        sphero.power.enter_soft_sleep()


if __name__ == "__main__":
    main()
