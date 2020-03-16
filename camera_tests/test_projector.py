from projector import Projector
from cueball import Cueball
import cv2

import numpy as np

p = Projector()
color = p.camera.getColorImage()
img = p.blankScreen()

c = Cueball()

cv2.namedWindow("window",cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
angle = 0
while(1):
    cv2.imshow("window", img)
    k = cv2.waitKey(33)
    if k == 27:
        break
    if k & 0b11111111 == ord('q'):
        sphero = p.findSphero()
        print("Current center sphero pixels is: ({},{})".format(sphero[0], sphero[1]))
        img = p.projectSpheroLine(sphero)
    elif k & 0b11111111 == ord('z'):
        img = p.blankScreen()
    elif k & 0b11111111 == ord('a'):
        angle = int(input("Input new angle between 0 and 360: "))
        img = p.projectSpheroLine(sphero,angle, True)
        c.rotate_cue(angle)
    elif k & 0b11111111 == ord('s'):
        power = int(input("Input power between 0 and 100: "))
        power = int(float(power) * 2.55)
        c.drive_until_collision(power, angle)
        sleep(3)
        c.align_to_north()
        img = p.projectSpheroLine(sphero)
    # CALIBRATION PURPOSES ONLY, SHOULD DELETE BEFORE MERGING TO MASTER
    
    #Change the short(width) offset
    elif k & 0b11111111 == ord('w'):
        print("Current s: {} l:{}".format(p.s, p.l))
        p.s = int(input("Enter the new s value: "))
        #While doing this, calibrate must be true so as to not call the find closest function
        p.projectSpheroLine(sphero, calibrate=True)
    #Change the long offset
    elif k & 0b11111111 == ord('l'):
        print("Current s: {} l: {}".format(p.s, p.l))
        p.l = int(input("Enter the new l value: "))
        p.projectSpheroLine(sphero, calibrate=True)

cv2.destroyAllWindows()
