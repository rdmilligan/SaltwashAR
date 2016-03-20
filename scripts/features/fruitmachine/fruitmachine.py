# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import *
from detection import Detection
import numpy as np
from reels import *
from random import randint
import time
from constants import *

class FruitMachine(Feature, Speaking, Emotion):

    def __init__(self, text_to_speech, speech_to_text):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        Emotion.__init__(self)
        self.speech_to_text = speech_to_text
        self.background_image = np.array([])
        self.detection_image = np.array([])
        self.detection = Detection()
        self.reels = [None, None, None]
        self.holds = [None, None]
        self.coins = 100

    # start thread
    def start(self, args=None):
        Feature.start(self, args)
        self.background_image = args
        self.detection_image = args.copy()

        # draw holds
        self.background_image = draw_holds(self.holds, self.background_image)

        # rotate and draw reels
        self.reels = rotate_reels(self.reels)
        draw_reels(self.reels)

    # stop thread
    def stop(self):
        Feature.stop(self)
        self.background_image = np.array([])

    # run thread
    def _thread(self, args):

        # check player has coins
        if self.coins == 0:
            self._text_to_speech("Sorry dude, you're all out of cash")
            return

        # on occasion, allow player to hold reels
        if (not None in self.reels) and (randint(0,2) == 0):

            # croupier tells player that one or two reels can be held
            self._text_to_speech("If you want to hold one or two fruits, press them now")

            # player selects holds
            self.detection.set_previous_image(self.detection_image)

            for i, hold in enumerate(self.holds):
                timeout = time.time() + 5

                while True:
                    active_cell = self.detection.get_active_cell(self.detection_image)

                    if (active_cell != None) and (active_cell not in self.holds):
                        self.holds[i] = active_cell
                        break

                    if time.time() > timeout:
                        break

                if self.holds[i] == None: break

        # croupier asks player if ready to spin reels
        self._text_to_speech("Just say the word Start, and I'll spin the fruits")

        # wait until player says "start"
        while self.speech_to_text.convert() != "start": continue

        # refresh reels
        self.reels = refresh_reels(self.reels, self.holds)

        # wait while reels rotate
        while is_reels_rotating(self.reels):
            time.sleep(1)

        # clear any holds
        self.holds = [None, None]

        # determine if player has won or lost
        if is_reels_win(self.reels):
            self.coins += 50
            self._text_to_speech("Wow, you won! You now have {} coins".format(self.coins))
            self._display_emotion(HAPPY)
        else:
            self.coins -= 10
            self._text_to_speech("Damn, you lost! You now have {} coins".format(self.coins))
            self._display_emotion(SAD)