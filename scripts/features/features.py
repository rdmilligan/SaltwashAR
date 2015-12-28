from constants import *

class Features:

    # initialise features
    def __init__(self, config_provider):

        text_to_speech = None
        if config_provider.browser or config_provider.hand_gesture or config_provider.play_your_cards_right:
            from shared import TextToSpeech
            text_to_speech = TextToSpeech()

        speech_to_text = None
        if config_provider.browser or config_provider.play_your_cards_right:
            from shared import SpeechToText
            speech_to_text = SpeechToText()

        self.browser = None
        if config_provider.browser:
            from browser import Browser
            self.browser = Browser(text_to_speech, speech_to_text)

        self.hand_gesture = None
        if config_provider.hand_gesture:
            from handgesture import HandGesture
            self.hand_gesture = HandGesture(text_to_speech)

        self.play_your_cards_right = None
        if config_provider.play_your_cards_right:
            from playyourcardsright import PlayYourCardsRight
            self.play_your_cards_right = PlayYourCardsRight(text_to_speech, speech_to_text)

    # indicate whether a feature is speaking
    def is_speaking(self):
        return (self.browser and self.browser.is_speaking) \
                or (self.hand_gesture and self.hand_gesture.is_speaking) \
                or (self.play_your_cards_right and self.play_your_cards_right.is_speaking)

    # provide emotion from a feature
    def get_emotion(self):
        if self.hand_gesture: 
            return self.hand_gesture.emotion

        return None

    # handle features
    def handle(self, rocky_robot_is_facing, sporty_robot_is_facing, image):
        self._handle_browser(rocky_robot_is_facing, sporty_robot_is_facing)
        self._handle_hand_gesture(rocky_robot_is_facing, sporty_robot_is_facing, image)
        self._handle_play_your_cards_right(sporty_robot_is_facing)

    # handle browser
    def _handle_browser(self, rocky_robot_is_facing, sporty_robot_is_facing):
        if not self.browser: return

        if rocky_robot_is_facing:
            self.browser.start(ROCK)
        elif sporty_robot_is_facing:
            self.browser.start(SPORT)
        else:
            self.browser.stop()

    # handle hand gesture
    def _handle_hand_gesture(self, rocky_robot_is_facing, sporty_robot_is_facing, image):
        if not self.hand_gesture: return

        if rocky_robot_is_facing or sporty_robot_is_facing:
            self.hand_gesture.start(image)
        else:
            self.hand_gesture.stop()

    # handle play your cards right
    def _handle_play_your_cards_right(self, sporty_robot_is_facing):
        if not self.play_your_cards_right: return

        if sporty_robot_is_facing:
            self.play_your_cards_right.start()
        else:
            self.play_your_cards_right.stop()

