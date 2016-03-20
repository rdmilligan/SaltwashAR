# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature, Speaking
import speech_recognition as sr
import pygame
from time import sleep

class MixingDesk(Feature, Speaking):

    GUITAR = 'guitar'
    GUITAR_FILENAME = 'scripts/features/mixingdesk/guitar.wav'

    DRUMS = 'drums'
    DRUMS_FILENAME = 'scripts/features/mixingdesk/drums.wav'

    def __init__(self, text_to_speech, speech_to_text):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        self.speech_to_text = speech_to_text
        self.recognizer = sr.Recognizer()
        pygame.mixer.init(frequency=8000)

    def _thread(self, args):
    
        # mixing desk asks for vocal
        self._text_to_speech("Sing the vocal now...")
    
        # user sings
        with sr.Microphone() as source:
            print "listening..."
            wav_data = self.recognizer.listen(source).get_wav_data()

        # check whether to stop thread
        if self.is_stop: return
      
        # mixing desk asks for instruments
        self._text_to_speech("What instruments do you want?")

        # user gives instruments
        instruments = self._speech_to_text()

        # mixing desk gets mixing...
        pygame.mixer.set_num_channels(3)
        
        vocals = pygame.mixer.Channel(0)
        vocals.set_volume(0.8)       
        vocals.play(pygame.mixer.Sound(wav_data))

        if self.GUITAR in instruments:
            guitar = pygame.mixer.Channel(1)
            guitar.set_volume(0.3)
            guitar.play(pygame.mixer.Sound(self.GUITAR_FILENAME))

        if self.DRUMS in instruments:
            drums = pygame.mixer.Channel(2)
            drums.set_volume(0.6)
            drums.play(pygame.mixer.Sound(self.DRUMS_FILENAME))

        while vocals.get_busy():
            continue

        if self.GUITAR in instruments:
            guitar.stop()

        if self.DRUMS in instruments:
            drums.stop()

        sleep(4)

    def _speech_to_text(self):
        text = self.speech_to_text.convert()
        if not text: return ''

        return text.lower().split()