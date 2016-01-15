# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

import pyttsx

class TextToSpeech:

    def __init__(self):
        self.pyttsx = pyttsx.init()
 
    # convert text to speech
    def convert(self, text):
        print text

        try:
            self.pyttsx.say(text)
            self.pyttsx.runAndWait()
        except RuntimeError:
            print "Could not convert text to speech"