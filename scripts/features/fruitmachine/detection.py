# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

import cv2
import numpy as np

class Detection(object):
 
    THRESHOLD = 1500
 
    def __init__(self):
        self.previous_gray = None
 
    def set_previous_image(self, image):
        self.previous_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def get_active_cell(self, image):
        
        # obtain motion between previous and current image
        current_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        delta = cv2.absdiff(self.previous_gray, current_gray)
        threshold_image = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]

        # set cell height and width
        height, width = threshold_image.shape[:2]
        cell_height = height/2
        cell_width = width/3
 
        # store motion level for each cell
        cells = np.array([0, 0, 0])
        cells[0] = cv2.countNonZero(threshold_image[cell_height:height, 0:cell_width])
        cells[1] = cv2.countNonZero(threshold_image[cell_height:height, cell_width:cell_width*2])
        cells[2] = cv2.countNonZero(threshold_image[cell_height:height, cell_width*2:width])
 
        # obtain the most active cell
        top_cell =  np.argmax(cells)
 
        # return the most active cell, if threshold met
        if(cells[top_cell] >= self.THRESHOLD):
            return top_cell
        else:
            return None