# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import *
from constants import *

class Acting(Feature, Speaking, Emotion):

    BOT_TAG = '[walter]'
    HUMAN_TAG = '[dude]'

    def __init__(self, text_to_speech, speech_to_text):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        Emotion.__init__(self)
        self.speech_to_text = speech_to_text
        self.script = self._load_script()
        self.fluffed_lines_count = 0

    # load script
    def _load_script(self):
        with open('scripts/features/acting/script.txt') as script_file:
            return script_file.readlines()

    # run thread
    def _thread(self, args):
        
        # check for end of script 
        if not self.script: return

        # get next line from script
        line = self.script[0].replace('\n', '')
        tag_end_index = line.rfind(']')
        tags = line[:tag_end_index + 1]
        words = line[tag_end_index + 1:]

        # bot delivers a line from script
        if self.BOT_TAG in tags:
            self._text_to_speech(words)

            if HAPPY in tags:
                self._display_emotion(HAPPY)
            elif SAD in tags:
                self._display_emotion(SAD)
            elif ANGRY in tags:
                self._display_emotion(ANGRY)
 
        # human delivers a line from script       
        elif self.HUMAN_TAG in tags:
            human_words = self.speech_to_text.convert()

            if not human_words or human_words.lower() != words.lower():
                self.fluffed_lines_count += 1

        # remove line from script
        del self.script[0]

        # if end of script, inform user of fluffed lines
        if not self.script:
            self._text_to_speech("You fluffed your lines {} times".format(self.fluffed_lines_count))