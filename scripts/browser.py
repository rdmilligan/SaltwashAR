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
         
    # create thread for processing content
    def start(self):
        Thread(target=self._process, args=()).start()

    def _process(self):
        while True:
            if self.category:
                # store current category
                current_category = self.category

                # browser asks question
                self.text_to_speech.convert('What do you want to load, buddy?')

                # user gives answer
                answer = self.speech_to_text.convert()
                if not answer: continue

                # get url from search engine
                url = search_engine(self.category, answer)
                if not url: continue

                # browser tells user that content is being retrieved
                self.text_to_speech.convert("Cool. I will get you stuff now...")

                # get web content
                request = requests.get(url)
                soup = BeautifulSoup(request.text) 

                # get text from web content
                [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
                text = soup.getText()
                
                # speak each line of text        
                try:
                    for line in text.split('\n'):
                        if self.category != current_category: break
                                
                        if len(line) >= self.MIN_LINE_LENGTH:
                            self.text_to_speech.convert(line)
                except:
                    print "Browser: error converting text to speech"

    # load
    def load(self, category):
        self.category = category

    # halt
    def halt(self):
        self.category = None




