from projector import Projector
import cv2

import numpy as np

p = Projector()
color = p.camera.getColorImage()
img = p.blankScreen()

cv2.namedWindow("window",cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
while(1):
    cv2.imshow("window", img)
    k = cv2.waitKey(33)
    if k == 27:
        break
    if k & 0b11111111 == ord('q'):
        sphero = p.findSphero()
        img = p.projectSpheroLine(sphero)
    elif k & 0b11111111 == ord('z'):
        img = p.blankScreen()
    elif k & 0b11111111 == ord('a'):
        angle = int(input("Input new angle between 0 and 360: "))
        img = p.projectSpheroLine(sphero,angle, True)
        
cv2.destroyAllWindows()
