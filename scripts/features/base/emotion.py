from feature import Feature
from constants import *
from time import sleep

class Emotion:
  
    # initialize emotion
    def __init__(self):
        self.emotion = None

    # display emotion
    def _display_emotion(self, emotion):
        self.emotion = emotion
        sleep(EMOTION_DISPLAYTIME)
        self.emotion = None