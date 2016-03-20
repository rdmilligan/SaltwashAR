# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature, Speaking
from shapesfunctions import *
import numpy as np
import cv2
from threading import Thread
from time import sleep

class Shapes(Feature, Speaking):

    # region of interest constants
    TOP_BORDER = 10
    BOTTOM_BORDER = 10
    LEFT_BORDER = 10
    RIGHT_BORDER = 10

    # shape constants
    TRIANGULAR_POINTS = 3
    QUADRILATERAL_POINTS = 4
    SHAPE_MIN_AREA = 100

    def __init__(self, text_to_speech):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        self.is_pyramid = False
        self.is_cube = False
        self.rotation = 0
        self.background_image = np.array([])
        self.speech_thread = None

    # start thread
    def start(self, args=None):
        Feature.start(self, args)
 
        # draw rotating pyramid or cube
        self.rotation += 1

        if self.is_pyramid:
            draw_pyramid(self.rotation)
        elif self.is_cube:
            draw_cube(self.rotation)

    # stop thread
    def stop(self):
        Feature.stop(self)
        self.background_image = np.array([])

    # run thread
    def _thread(self, args):
        image = args
        
        # get region of interest
        height, width = image.shape[:2]
        roi = image[self.TOP_BORDER:height-self.BOTTOM_BORDER, self.LEFT_BORDER:width-self.RIGHT_BORDER]

        # detect edges
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        edges = cv2.Canny(gray, 100, 200)

        # get contours
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:6]

        # find shape
        shape_contour = np.array([])
        shape_points = 0

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01*perimeter, True)
            shape_points = len(approx)

            if shape_points == self.TRIANGULAR_POINTS or shape_points == self.QUADRILATERAL_POINTS:
                shape_contour = contour
                break       

        # if shape found...
        if shape_contour.size > 0 and cv2.contourArea(shape_contour) >= self.SHAPE_MIN_AREA: 

            # draw green line around shape
            cv2.drawContours(roi, shape_contour, -1, (0, 255, 0), 3)
            image[self.TOP_BORDER:height-self.BOTTOM_BORDER, self.LEFT_BORDER:width-self.RIGHT_BORDER] = roi
            self.background_image = image

            # draw pyramid or cube
            text = None

            if shape_points == self.TRIANGULAR_POINTS:
                self.is_pyramid = True
                self.is_cube = False
                text = "You have drawn a triangle, which has helped me build this lovely pyramid"
            else:
                self.is_pyramid = False
                self.is_cube = True
                text = "You have sketched a square, which I have used six times to build this cube"
     
            # tell user about shape
            if not self.speech_thread or not self.speech_thread.is_alive():
                self.speech_thread = Thread(target=self._speech_thread, args=(text,))
                self.speech_thread.start()        
        else:
            self.is_pyramid = False
            self.is_cube = False
            self.background_image = np.array([])

    # speech thread
    def _speech_thread(self, text):
        self._text_to_speech(text)
        sleep(4)
    