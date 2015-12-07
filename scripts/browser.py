from threading import Thread
import requests
from bs4 import BeautifulSoup
from texttospeech import TextToSpeech
from speechtotext import SpeechToText
from searchdatabase import *
from constants import *

class Browser:

    MIN_LINE_LENGTH = 60
       
    def __init__(self):
        self.text_to_speech = TextToSpeech()
        self.speech_to_text = SpeechToText()
        self.category = None
        self.is_speaking = False

    # create thread for processing content
    def start(self):
        Thread(target=self._process, args=()).start()

    def _process(self):
        while True:
            if self.category:
                # obtain current category
                current_category = self.category

                # browser asks question
                self._text_to_speech("What do you want to load, buddy?")

                # user gives answer
                answer = self.speech_to_text.convert()
                if not answer: continue

                # get url from search engine
                url = search_engine(current_category, answer)
                if not url: continue

                # browser tells user that content is being retrieved
                self._text_to_speech("Cool. I will get you stuff now...")

                # get web content
                request = requests.get(url)
                soup = BeautifulSoup(request.text) 

                # get text from web content
                [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
                text = soup.getText()
                
                # speak each line of text        
                try:
                    for line in text.split('\n'):
                        if current_category != self.category: break
                                
                        if len(line) >= self.MIN_LINE_LENGTH:
                            self._text_to_speech(line)
                except:
                    print "Browser: error converting text to speech"
    
    # text to speech
    def _text_to_speech(self, text):
        self.is_speaking = True
        self.text_to_speech.convert(text)
        self.is_speaking = False

    # load
    def load(self, category):
        self.category = category

    # halt
    def halt(self):
        self.category = None




