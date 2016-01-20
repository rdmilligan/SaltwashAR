# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import *
import ConfigParser
import numpy as np
import cv2
from constants import *

class HappyColour(Feature, Speaking, Emotion):
  
    def __init__(self, text_to_speech):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        Emotion.__init__(self)
        self._load_config()

    def _load_config(self):
        config = ConfigParser.ConfigParser()
        config.read('scripts/features/happycolour/happycolour.ini')
        
        # get colour range from config
        self.lower_colour = np.array(map(int, config.get('Colour', 'Lower').split(',')))
        self.upper_colour = np.array(map(int, config.get('Colour', 'Upper').split(',')))

        # get threshold from config
        self.lower_threshold = config.getint('Threshold', 'Lower')
        self.upper_threshold = config.getint('Threshold', 'Upper')

    def _thread(self, args):
        image = args

        # convert image from BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # only get colours in range
        mask = cv2.inRange(hsv, self.lower_colour, self.upper_colour)

        # obtain colour count
        colour_count = cv2.countNonZero(mask)

        # check whether to stop thread
        if self.is_stop: return

        # respond to colour count
        if colour_count < self.lower_threshold:
            self._text_to_speech("I just feel sad")
            self._display_emotion(SAD)
        elif colour_count > self.upper_threshold:
            self._text_to_speech("I'm so happy!")
            self._display_emotion(HAPPY)