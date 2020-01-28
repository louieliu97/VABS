from time import sleep

from pysphero.core import Sphero


def main():
    mac_address = "F1:B6:E8:5A:7B:D7" #Sphero 1
    #wmac_address = "F1:8D:AE:17:9D:75" #Sphero 2
    with Sphero(mac_address=mac_address) as sphero:
        sphero.power.wake()
        sleep(2)
        sphero.power.enter_soft_sleep()


if __name__ == "__main__":
    main()
