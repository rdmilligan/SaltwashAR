from constants import *
from browser import Browser
from handgesture import HandGesture

class Features:

    def __init__(self, config_provider):
        # initialise browser
        self.browser = None
        
        if config_provider.browser:
            self.browser = Browser()

        # initialise hand gesture
        self.hand_gesture = None
        
        if config_provider.hand_gesture:
            self.hand_gesture = HandGesture()

    # indicate whether a feature is speaking
    def is_speaking(self):
        return (self.browser and self.browser.is_speaking) \
                or (self.hand_gesture and self.hand_gesture.is_speaking)

    # provide an emotion from feature
    def get_emotion(self):
        if self.hand_gesture: return self.hand_gesture.emotion

    def handle(self, rocky_robot_is_facing, sporty_robot_is_facing, image):
        # handle browser
        self._handle_browser(rocky_robot_is_facing, sporty_robot_is_facing)

        # handle hand gesture
        self._handle_hand_gesture(rocky_robot_is_facing, sporty_robot_is_facing, image)

    def _handle_browser(self, rocky_robot_is_facing, sporty_robot_is_facing):
        # check browser instantiated
        if not self.browser: return

        # handle browser
        if rocky_robot_is_facing:
            self.browser.start(ROCK)
        elif sporty_robot_is_facing:
            self.browser.start(SPORT)
        else:
            self.browser.stop()

    def _handle_hand_gesture(self, rocky_robot_is_facing, sporty_robot_is_facing, image):
        # check hand gesture instantiated
        if not self.hand_gesture: return

        # handle hand gesture
        if rocky_robot_is_facing or sporty_robot_is_facing:
            self.hand_gesture.start(image)
        else:
            self.hand_gesture.stop()

