# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature, Speaking
from neuraldata import *
from neuralnetwork import *
from time import sleep

class AudioClassifier(Feature, Speaking):

    def __init__(self, text_to_speech):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        self.neural_network = None

    # run thread
    def _thread(self, args):

        # request audio data from user
        input,_ = create_data(self._text_to_speech)

        # check audio data okay
        if not input:
            print "The data you have provided is not valid"
            return

        # ensure neural network has been built
        if not self.neural_network:
            inputs,targets = load_data()
            self.neural_network = build_network(inputs,targets)

        # check whether to stop thread
        if self.is_stop: return

        # classify audio data
        audio_index = classify_data(self.neural_network, input)

        # inform user of audio classification
        self._text_to_speech("Your audio data has been classified as {}".format(AUDIO_CLASSES[audio_index]))
        sleep(6)