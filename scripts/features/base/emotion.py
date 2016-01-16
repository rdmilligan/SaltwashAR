# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from time import sleep

class Emotion:

    # initialize emotion
    def __init__(self):
        self.emotion = None

    # display emotion
    def _display_emotion(self, emotion):
        self.emotion = emotion
        sleep(2)
        self.emotion = None