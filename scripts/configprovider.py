# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

import ConfigParser

class ConfigProvider:

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("appsettings.ini")

    @property
    def animation(self):
        return self.config.getboolean("Enhancements", "Animation")

    @property 
    def browser(self):
        return self.config.getboolean("Features", "Browser")

    @property
    def calculator(self):
        return self.config.getboolean("Features", "Calculator")

    @property 
    def hand_gesture(self):
        return self.config.getboolean("Features", "HandGesture")

    @property 
    def happy_colour(self):
        return self.config.getboolean("Features", "HappyColour")

    @property 
    def mixing_desk(self):
        return self.config.getboolean("Features", "MixingDesk")

    @property 
    def optical_character_recognition(self):
        return self.config.getboolean("Features", "OpticalCharacterRecognition")

    @property 
    def phrase_translation(self):
        return self.config.getboolean("Features", "PhraseTranslation")

    @property 
    def play_your_cards_right(self):
        return self.config.getboolean("Features", "PlayYourCardsRight")

    @property 
    def television(self):
        return self.config.getboolean("Features", "Television")