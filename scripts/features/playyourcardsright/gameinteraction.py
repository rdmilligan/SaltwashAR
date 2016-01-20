# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Speaking

class GameInteraction(Speaking):
 
    def __init__(self, text_to_speech, speech_to_text):
        Speaking.__init__(self, text_to_speech)
        self.speech_to_text = speech_to_text
 
    # 13 states
    CARD = {
        '2': [0.0],
        '3': [1.0],
        '4': [2.0],
        '5': [3.0],
        '6': [4.0],
        '7': [5.0],
        '8': [6.0],
        '9': [7.0],
        '10': [8.0],
        'jack': [9.0],
        'queen': [10.0],
        'king': [11.0],
        'ace': [12.0]
        }
 
    # 2 actions
    COMMAND = {
        0.0: 'lower',
        1.0: 'higher'
        }
 
    # 2 rewards
    RESULT = {
        'no': -1.0,
        'yes': 1.0
        }
 
    def get_card(self):
             
        # ask user for card
        self._text_to_speech("What card do you have?")
         
        # wait for user's response
        response = ''
        while response not in self.CARD:
            response = self._speech_to_text()
 
        return self.CARD[response]
 
    def give_command(self, action):
         
        # get command
        command_key = float(action)
        command = ''
 
        if command_key in self.COMMAND:
            command = self.COMMAND[command_key]
 
        # give command to user
        self._text_to_speech(command)
         
    def get_result(self):
         
        # ask user for result
        self._text_to_speech("Did you win the turn?")
 
        # wait for user's response
        response = ''
        while response not in self.RESULT:
            response = self._speech_to_text()
 
        return self.RESULT[response]

    def _speech_to_text(self):
        text = self.speech_to_text.convert()
        if not text: return ''

        return text.lower()