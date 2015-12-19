from threading import Thread
import cv2
from ..shared import TextToSpeech

class HandGesture:
  
    def __init__(self):
        self.thread = None
        self.is_stop = False
        self.is_speaking = False
        self.text_to_speech = TextToSpeech()

    def start(self, image):
        self.is_stop = False
        
        if self.thread and self.thread.is_alive(): return

        self.thread = Thread(target=self._thread, args=(image,))
        self.thread.start()

    def stop(self):
        self.is_stop = True

    def _thread(self, image):
        
        # detect hand gesture in image
        is_okay = self._is_item_detected_in_image('classifiers/haarcascade_okaygesture.xml', image.copy())
        is_vicky = self._is_item_detected_in_image('classifiers/haarcascade_vickygesture.xml', image.copy())

        # check whether to stop thread
        if self.is_stop: return

        # respond to hand gesture
        if is_okay:
            self._text_to_speech("Hi there, buddy")
        elif is_vicky:
            self._text_to_speech("Well, there is no need to be so rude!")

    def _is_item_detected_in_image(self, classifier_path, image):

        classifier = cv2.CascadeClassifier(classifier_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        items = classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=4, minSize=(200, 260))

        return len(items) > 0

    def _text_to_speech(self, text):
        self.is_speaking = True
        self.text_to_speech.convert(text)
        self.is_speaking = False
 




