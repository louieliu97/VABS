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
        table_img = self.camera.getColorImage()
        
        center = [int(table_img.shape[0]/2), int(table_img.shape[1]/2)]

        #convert image to hsv
        hsv = cv2.cvtColor(table_img.copy(), cv2.COLOR_BGR2HSV)
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
            areas.append(cv2.contourArea(c))

        maxContour = contours[np.argmax(np.array(areas))]

        # Find the convex hull of the maxContour since the contour isn't likely to have
        # very straight lines
        hull = cv2.convexHull(maxContour)
        #cv2.drawContours(table_img, maxContour, -1, (0,255,0), 1)
        #cv2.drawContours(table_img, [hull], -1, (255,0,0), 1)

        return [hull]

    def findSphero(self):
        """
        This function will find the center pixel position of the sphero from a color image

        @params None

        @return pixel: The pixel in the image containing the center of the sphero
        """

        cimg = self.camera.getColorImage()

        #convert to grayscale for HoughCircles
        img = cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)

        circles = np.asarray(cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1, 5,
                            param1=40, param2=30, minRadius=15, maxRadius=30))
        # The return array from opencv functions puts the end list inside another
        # list, which makes it difficult to deal with, so we reshape.
        circles = circles.reshape((circles.shape[1], circles.shape[2]))
        # We order by the 3rd column which is radius, since we know that the sphero
        # has the largest radius.
        circles = circles[circles[:,2].argsort()]
        print(circles)

        for i in circles:
            #draw outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0,255,0), 2)
            
            #draw center of circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0,0,255), 3)

        s = circles[-1]
        cv2.circle(cimg, (s[0], s[1]), s[2], (255, 0, 0), 2)
        cv2.circle(cimg, (s[0], s[1]), 2, (0,255,0), 3)

        cv2.imshow('',cimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
