# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import *
import cv2
from constants import *

class HandGesture(Feature, Speaking, Emotion):
  
    def __init__(self, text_to_speech):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        Emotion.__init__(self)

    def _thread(self, args):
        image = args

        # detect hand gesture in image
        is_okay = self._is_item_detected_in_image('scripts/features/handgesture/haarcascade_okaygesture.xml', image)
        is_vicky = self._is_item_detected_in_image('scripts/features/handgesture/haarcascade_vickygesture.xml', image)

        # check whether to stop thread
        if self.is_stop: return

        # respond to hand gesture
        if is_okay:
            self._text_to_speech("Hi there, buddy")
            self._display_emotion(HAPPY)
        elif is_vicky:
            self._text_to_speech("Well, there is no need to be so rude!")
            self._display_emotion(ANGRY)

    def _is_item_detected_in_image(self, classifier_path, image):

        classifier = cv2.CascadeClassifier(classifier_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        items = classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=4, minSize=(200, 260))

        return len(items) > 0