##################################################################################
# Title: camera.py
# Author: Louie Liu
# Date: 15 April 2020
##################################################################################

import cv2
import pyrealsense2 as rs

import numpy as np

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        cimg = np.asanyarray(color_frame.get_data())
        img = cv2.cvtColor(cimg,cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,5,param1=40,param2=30,minRadius=10,maxRadius=30)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                #draw outer circle
                cv2.circle(cimg, (i[0], i[1]), i[2], (0,255,0), 2)

                #draw center of circle
                cv2.circle(cimg, (i[0], i[1]), 2, (0,0,255), 3)
    
        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', cimg)
        if cv2.waitKey(1) == 27:
            break
finally:
    pipeline.stop()

cv2.destroyAllWindows()
