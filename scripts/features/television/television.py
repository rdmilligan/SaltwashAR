# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature
import numpy as np
import cv2
from televisionfunctions import *

class Television(Feature):

    QUADRILATERAL_POINTS = 4
    BLACK_THRESHOLD = 100
    WHITE_THRESHOLD = 155
    TELEVISION_PATTERN = [1, 0, 1, 0, 1, 0, 1, 0, 1]

    def __init__(self):
        Feature.__init__(self)
        self.background_image = np.array([])
        self.video_capture = cv2.VideoCapture()

    # stop thread
    def stop(self):
        Feature.stop(self)
        
        self.background_image = np.array([])

        if self.video_capture.isOpened():
            self.video_capture.release()

    # get latest frame from video
    def _get_video_frame(self):

        success, frame = self.video_capture.read()
        if success: return frame

        if not self.video_capture.isOpened():
            self.video_capture.open('scripts/features/television/channel_one.mp4')
        else:
            self.video_capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)      

        return self.video_capture.read()[1]

    def _thread(self, args):
        image = args

        # Stage 1: Detect edges in image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        edges = cv2.Canny(gray, 100, 200)

        # Stage 2: Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        for contour in contours:

            # Stage 3: Shape check
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01*perimeter, True)

            if len(approx) == self.QUADRILATERAL_POINTS:

                # Stage 4: Perspective warping
                topdown_quad = get_topdown_quad(gray, approx.reshape(4, 2))

                # Stage 5: Border check
                if topdown_quad[(topdown_quad.shape[0]/100.0)*5, 
                                (topdown_quad.shape[1]/100.0)*5] > self.BLACK_THRESHOLD: continue

                # Stage 6: Get marker pattern
                marker_pattern = None
                
                try:
                    marker_pattern = get_marker_pattern(topdown_quad, self.BLACK_THRESHOLD, self.WHITE_THRESHOLD)
                except:
                    continue
                
                if not marker_pattern: continue

                # Stage 7: Match marker pattern
                if marker_pattern != self.TELEVISION_PATTERN: continue

                # Stage 8: Substitute marker
                if self.is_stop: return

                self.background_image = add_substitute_quad(image, self._get_video_frame(), approx.reshape(4, 2))
                return
    
        self.background_image = np.array([])
