from feature import Feature

class Speaking:
  
    # initialize speaking
    def __init__(self, text_to_speech):
        self.is_speaking = False
        self.text_to_speech = text_to_speech

    # text to speech
    def _text_to_speech(self, text):
        self.is_speaking = True
        self.text_to_speech.convert(text)
        self.is_speaking = False