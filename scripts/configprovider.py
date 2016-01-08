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
    def hand_gesture(self):
        return self.config.getboolean("Features", "HandGesture")

    @property 
    def play_your_cards_right(self):
        return self.config.getboolean("Features", "PlayYourCardsRight")

    @property 
    def happy_colour(self):
        return self.config.getboolean("Features", "HappyColour")

    @property 
    def optical_character_recognition(self):
        return self.config.getboolean("Features", "OpticalCharacterRecognition")

    @property 
    def television(self):
        return self.config.getboolean("Features", "Television")

    @property 
    def phrase_translation(self):
        return self.config.getboolean("Features", "PhraseTranslation")