# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature, Speaking
from searchdatabase import *
import requests
from bs4 import BeautifulSoup

class Browser(Feature, Speaking):

    MIN_LINE_LENGTH = 60
       
    def __init__(self, text_to_speech, speech_to_text):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        self.speech_to_text = speech_to_text

    def _thread(self, args):
        category = args

        # browser asks question
        self._text_to_speech("What do you want to load, buddy?")

        # user gives answer
        answer = self.speech_to_text.convert()
        if not answer: return

        # get url from search engine
        url = search_engine(category, answer)
        if not url: return

        # browser tells user that content is being retrieved
        self._text_to_speech("Cool. I will get you stuff now...")

        # get web content
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'lxml') 

        # get text from web content
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        text = soup.getText()
                
        # speak each line of text        
        try:
            for line in text.split('\n'):
                if self.is_stop: return
                                
                if len(line) >= self.MIN_LINE_LENGTH:
                    self._text_to_speech(line)
        except:
            print "Browser: error converting text to speech"