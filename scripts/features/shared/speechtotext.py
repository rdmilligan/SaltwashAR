# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

import speech_recognition as sr

class SpeechToText:

    def __init__(self):
        self.recognizer = sr.Recognizer()
 
    # convert speech to text
    def convert(self):

        with sr.Microphone() as source:
            print "listening..."
            audio = self.recognizer.listen(source)

        text = None

        try:
            text = self.recognizer.recognize_google(audio)
            print text
        except sr.UnknownValueError:
            print "Google Speech Recognition could not understand audio"
        except sr.RequestError:
            print "Could not request results from Google Speech Recognition service"

        return text
