

import cv2
import pyrealsense2 

import numpy as np

from camera import Camera

class Projector:

    def __init__(self):
        self.camera = Camera()

    def getTableSegment(self):
        """
        This function gets the segment of the image that is the table (the felted area)

        @params None

        @returns the convex hull containing the relevant part of the image
        """
        color_img = self.camera.getColorImage()
        center = [int(color_image.shape[0]/2), int(color_image.shape[1]/2)]

        #convert image to hsv
        hsv = cv2.cvtColor(table_image.copy(), cv2.COLOR_BGR2HSV)
        search_width = 50
        h,s,v = hsv[center[0]][center[1]]

        # Create the upper and lower bounds for the color at the center of the tabel
        lower_color = np.array([h-search_width,s-search_width,v-search_width])
        upper_color = np.array([h+search_width,s+search_width,v+search_width])

        #Find all the pixels that are within the range specified
        mask = cv2.inRange(hsv, lower_color, upper_color)
        #MedianBlur to remove speckling
        median = cv2.medianBlur(mask, 7)
        #Find all contours of the pixels in the range
        contours, _ = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #Find the contour with the largest area. This is the pool table surface
        areas = []
        for c in contours:
            maxContour = contours[np.argmax(np.array(areas))]
        img = np.zeros(shape)

        # Find the convex hull of the maxContour since the contour isn't likely to have
        # very straight lines
        hull = cv2.convexHull(maxContour)
        cv2.drawContours(table_img, maxContour, -1, (0,255,0), 1)
        cv2.drawContours(table_img, [hull], -1, (255,0,0), 1)

        
