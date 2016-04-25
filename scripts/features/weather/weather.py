# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature, Speaking
from OpenGL.GL import *
from urllib2 import urlopen
import json
from time import sleep

class Weather(Feature, Speaking):

    # Attention: visit https://www.worldweatheronline.com/ to register for a free API key
    
    WEATHER_API_KEY = None 
    WEATHER_API = 'http://api.worldweatheronline.com/free/v1/weather.ashx?q={}&format=json&num_of_days=1&key={}'
    CLOUDY_TERMS = ['partly cloudy', 'mist', 'fog', 'overcast']

    def __init__(self, text_to_speech, speech_to_text):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        self.speech_to_text = speech_to_text
        self.is_cloudy = False

    # start thread
    def start(self, args=None):
        Feature.start(self, args)
 
        # enable fog if cloudy
        if self.is_cloudy:
            glFogi(GL_FOG_MODE, GL_LINEAR)
            glFogfv(GL_FOG_COLOR, (0.5, 0.5, 0.5, 1.0))
            glFogf(GL_FOG_DENSITY, 0.35)
            glHint(GL_FOG_HINT, GL_NICEST)
            glFogf(GL_FOG_START, 1.0)
            glFogf(GL_FOG_END, 5.0)
            glEnable(GL_FOG)
        else:
            glDisable(GL_FOG)

    # stop thread
    def stop(self):
        Feature.stop(self)
        
        # disable fog
        glDisable(GL_FOG)
        self.is_cloudy = False

    # run thread
    def _thread(self, args):
   
        # check for API key
        if not self.WEATHER_API_KEY:
            self._text_to_speech("You need to visit world weather online to register for a free API key")
            return
        
        # ask user for location
        self._text_to_speech("Which location would you like weather from?")

        # user replies with location
        location = self.speech_to_text.convert()
        if not location: return

        # fetch weather 
        weather_description = None
        url = self.WEATHER_API.format(location.replace (' ', '+'), self.WEATHER_API_KEY)

        try:
            response = urlopen(url)
            object = json.load(response)
            weather_description = object['data']['current_condition'][0]['weatherDesc'][0]['value'].strip().lower()
        except:
            print "Error getting weather"

        if not weather_description: return   

        # check whether to stop thread
        if self.is_stop: return

        # inform user of weather
        weather_report = 'The weather in {} is {}.'.format(location, weather_description)

        if weather_description in self.CLOUDY_TERMS:
            self.is_cloudy = True
            self._text_to_speech(weather_report + " It's real cloudy here.")
        else:
            self.is_cloudy = False
            self._text_to_speech(weather_report)

        sleep(4)