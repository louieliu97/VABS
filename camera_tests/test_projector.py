from projector import Projector
import cv2

import numpy as np

p = Projector()
hull = p.getTableSegment()
reorder_hull = p.order_corners(hull[0])
color = p.camera.getColorImage()
img = p.blankScreen(color.shape)
p.findSphero()

cv2.namedWindow("window",cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
while(1):
    cv2.imshow("window", img)
    k = cv2.waitKey(33)
    if k == 27:
        break
    elif k & 0b11111111 == ord('q'):
        sphero_point = p.findSphero()
        print("Sphero found")
        img = p.projectSpheroLine(sphero_point, img.shape, angle=270)
    elif k & 0b11111111 == ord('w'):
        img = p.blankScreen(color.shape)
        
cv2.destroyAllWindows()
