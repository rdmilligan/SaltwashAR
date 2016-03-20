# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature, Speaking
import numpy as np
from neuralnetwork import *
import cv2
from time import sleep

class IrisClassifier(Feature, Speaking):

    IRIS_CLASSES = ['setosa','versicolor','virginica']
    FEATURE_PATH = 'scripts/features/irisclassifier/'
    SLIDE_OFFSET = 50

    def __init__(self, text_to_speech, speech_to_text):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        self.speech_to_text = speech_to_text
        self.neural_network = None
        self.background_image = np.array([])
        self.iris_slide = np.array([])

    # start thread
    def start(self, args=None):
        image = args
        Feature.start(self, args)
 
        # if slide, add to background image
        if self.iris_slide.size > 0:
            slide_offset_and_height = self.SLIDE_OFFSET + self.iris_slide.shape[0]
            slide_offset_and_width = self.SLIDE_OFFSET + self.iris_slide.shape[1] 
        
            image[self.SLIDE_OFFSET:slide_offset_and_height, self.SLIDE_OFFSET:slide_offset_and_width] = self.iris_slide
            self.background_image = image
        else:
            self.background_image = np.array([])

    # stop thread
    def stop(self):
        Feature.stop(self)
        self.background_image = np.array([])

    # run thread
    def _thread(self, args):

        # request iris data from user
        sepal_length = self._request_iris_measurement("What is the sepal length in centimetres?")
        sepal_width =  self._request_iris_measurement("What is the sepal width in centimetres?")
        petal_length =  self._request_iris_measurement("What is the petal length in centimetres?")
        petal_width =  self._request_iris_measurement("What is the petal width in centimetres?")

        # check iris data okay
        if not sepal_length or not sepal_width or not petal_length or not petal_width:
            print "The data you have provided is not valid"
            return

        # ensure neural network has been built
        if not self.neural_network:
            self.neural_network = build_network()

        # check whether to stop thread
        if self.is_stop: return

        # classify iris data
        iris_index = classify_data(self.neural_network, [sepal_length, sepal_width, petal_length, petal_width])

        # update background image with iris slide
        self.iris_slide = cv2.imread('{}{}.jpg'.format(self.FEATURE_PATH, self.IRIS_CLASSES[iris_index]))

        # inform user of iris classification
        self._text_to_speech("Your iris data has been classified as {}".format(self.IRIS_CLASSES[iris_index]))
        sleep(6)

        # clear iris slide
        self.iris_slide = np.array([])

    # request iris data
    def _request_iris_measurement(self, request_message):

        self._text_to_speech(request_message)
        
        iris_measurement = self.speech_to_text.convert()

        try:
            return float(iris_measurement)
        except:
            return None


