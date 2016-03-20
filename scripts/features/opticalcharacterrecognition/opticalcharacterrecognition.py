# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature, Speaking
from pytesser import *

class OpticalCharacterRecognition(Feature, Speaking):
  
    # define region of interest
    TOP_BORDER = 10
    BOTTOM_BORDER = 10
    LEFT_BORDER = 20
    RIGHT_BORDER = 20

    def __init__(self, text_to_speech):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)

    def _thread(self, args):
        image = args
      
        # get region of interest
        height, width = image.shape[:2]
        roi = image[self.TOP_BORDER:height-self.BOTTOM_BORDER, self.LEFT_BORDER:width-self.RIGHT_BORDER]

        # convert image format
        roi = Image.fromarray(roi)     

        # get text from image
        text = image_to_string(roi)

        # convert text to speech
        self._text_to_speech(text)
