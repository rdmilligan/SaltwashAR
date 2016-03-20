# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature
import ConfigParser
import pygame

class PhraseTranslation(Feature):

    FILE_PATH = 'scripts/features/phrasetranslation/'

    def __init__(self, speech_to_text):
        Feature.__init__(self)
        self.is_speaking = False
        self.speech_to_text = speech_to_text
        self.phrases = self._load_config()
        pygame.mixer.init()

    # load phrases from config
    def _load_config(self):
        config = ConfigParser.ConfigParser()
        config.read('{}phrasetranslation.ini'.format(self.FILE_PATH))

        return dict(config.items('Phrases'))
    
    def _thread(self, args):
        
        # user speaks a phrase
        phrase = self.speech_to_text.convert()
        if not phrase: return

        # check whether to stop thread
        if self.is_stop: return

        # translator replies
        phrase = phrase.replace(' ', '').lower()
        sound_file = self.phrases.get(phrase)
 
        if sound_file:

            sound = pygame.mixer.Sound('{}{}'.format(self.FILE_PATH, sound_file))
            channel = sound.play()

            self.is_speaking = True

            while channel.get_busy():
                continue

            self.is_speaking = False
