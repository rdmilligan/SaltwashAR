import pyttsx

class TextToSpeech:

    def __init__(self):
        self.pyttsx = pyttsx.init()
 
    # convert text to speech
    def convert(self, text):
        print text

        self.pyttsx.say(text)
        self.pyttsx.runAndWait()

      