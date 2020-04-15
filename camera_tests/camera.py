##################################################################################
# Title: camera.py
# Author: Louie Liu
# Date: 15 April 2020
##################################################################################

import pyrealsense2 as rs

import numpy as np

class Camera:

    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

        self.pipeline.start(self.config)

    def getColorImage(self):
        """
        This function return a single color image from the realsense camera

        @params: None

        @returns: the color image
        """

        #Let auto-exposure settle down by waiting for multiple frames
        for i in range(20):
            frames = self.pipeline.wait_for_frames()
            
        color_frame = frames.get_color_frame()
        if not color_frame:
            raise ValueError("No color frame!")
        return np.asanyarray(color_frame.get_data())
