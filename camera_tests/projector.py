import math

import cv2
import pyrealsense2 

import numpy as np

from camera import Camera

class Projector:

    def __init__(self):
        self.camera = Camera()
        self.shape = self.camera.getColorImage().shape

        #Table for offsets
        self.table = np.genfromtxt('table.csv', delimiter=',')

        # Offsets used for accurate projection
        self.l = 0
        self.s = 0
        
    def getTableSegment(self):
        """
        This function gets the segment of the image that is the table (the felted area)
        
        @params None
        
        @returns the convex hull containing the relevant part of the image
        """
        table_img = self.camera.getColorImage()
        
        center = [int(self.shape[0]/2), int(self.shape[1]/2)]

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

        # Find the minimum rectangle that surrounds the maxContour since the contour
        # isn't likely to have very straight lines
        rect = cv2.minAreaRect(maxContour)
        box = np.int0(cv2.boxPoints(rect))
        return [box]

    def order_corners(self, pts):
        """
        Given the four points found for our contour, order them into
        Top Left, Top Right, Bottom Right, Bottom Left
        This order is important for perspective transforms

        :param pts: Contour points to be ordered correctly
        """
        rect = np.zeros((4,2), dtype=np.int16)

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def showImage(self,image, window=''):
        cv2.imshow(window, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def findSphero(self):
        """
        This function will find the center pixel position of the sphero from a color image

        @params None

        @return pixel: The pixel in the image containing the center of the sphero
        """
        
        while True:
            #convert to grayscale for HoughCircles
            img = cv2.cvtColor(self.camera.getColorImage(), cv2.COLOR_BGR2GRAY)
            circles = np.asarray(cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1, 2,
                                              param1=40, param2=30, minRadius=19, maxRadius=25))
            if circles.size <= 1:
                continue
            else:
                break
            
        # The return array from opencv functions puts the end list inside another
        # list, which makes it difficult to deal with, so we reshape.
        circles = circles.reshape((circles.shape[1], circles.shape[2]))
        # We order by the 3rd column which is radius, since we know that the sphero
        # has the largest radius.
        circles = circles[circles[:,2].argsort()]

        # The circle with the largest radius should be the sphero as it is larger
        # than any of the pool balls.
        return circles[-1]

    def findClosestPoint(self, point):
        """
        This function find a point in the table that is closest to the 
        input point.

        @param point:    The point to find the closest point to. The location 
                         of the sphero in the image
        
        @return closest[2]: The offset for the length
        @return closest[3]: The offset for the height
        """

        closest_dist = 9999999
        closest = None
        for t in self.table:
            dist = math.sqrt((t[1] - point[1])**2 + (t[0] - point[0])**2)
            if dist < closest_dist:
                closest_dist = dist
                closest = t

        return int(closest[2]), int(closest[3])
    
    def projectSpheroLine(self, point, angle=0):
        """
        This function uses the given sphero point to project a line at the given 
        angle starting from the sphero point.

        @param point: The pixel of the center of the sphero
        @param angle: The angle to shoot the sphero. Default is zero

        @return img: The image with the drawn circles and lines on it.
        """
        
        self.l,self.s = self.findClosestPoint((point[0], point[1]))
        # w and h are the width and height for a point slightly outside
        # the radius of the ball, but on the same line. This is for better
        # clarity and to ensure that the line does not overlap on top of
        # the sphero, but instead is slightly outside of it. This is the
        # start point of the line
        w = int(np.sin(np.deg2rad(angle)) * (point[2]+6))
        h = int(np.cos(np.deg2rad(angle)) * (point[2]+6))

        # These are the width and height values away from the center of the
        # sphero for the end point
        e_w = int(np.sin(np.deg2rad(angle)) * 100)
        e_h = int(np.cos(np.deg2rad(angle)) * 100)
        
  
        end = (int(point[0]+self.l) + e_w, int(point[1]+self.s) +e_h)

        #Draw the line
        img = np.zeros((self.shape), dtype=np.float32)
        cv2.line(img, (int(point[0]+self.l+w), int(point[1]+self.s+h)), end, (1,1,1), 4)

        #Draw outer circle
        cv2.circle(img,(int(point[0]+self.l), int(point[1])+self.s),int(point[2]*1.6),(1,1,1),4)

        return img


    def blankScreen(self):
        """
        This funciton creates a blank image in the given shape

        @return blank: The np array containing the blank image
        """
        
        blank = np.zeros((self.shape))
        blank.fill(255)
        return blank
        
        
