# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature, Speaking
 
class Calculator(Feature, Speaking):
 
    ADD = ['+', 'plus', 'added']
    SUBTRACT = ['-', 'minus', 'subtracted']
    MULTIPLY = ['x', 'times', 'multiplied']
    DIVIDE = ['/', 'divided']

    def __init__(self, text_to_speech, speech_to_text):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        self.speech_to_text = speech_to_text
     
    def _thread(self, args):
        # user provides expression
        expression = self.speech_to_text.convert()
        if not expression: return

        # check whether to stop thread
        if self.is_stop: return

        # calculate answer from expression
        expression = expression.lower().split()
        if len(expression) < 3: return       

        expression_left = expression[0]
        expression_middle = expression[1]
        expression_right = expression[-1]

        answer = None

        try:
            if expression_middle in self.ADD:
                answer = int(expression_left) + int(expression_right)
            elif expression_middle in self.SUBTRACT:
                answer = int(expression_left) - int(expression_right)
            if expression_middle in self.MULTIPLY:
                answer = int(expression_left) * int(expression_right)
            if expression_middle in self.DIVIDE:
                answer = int(expression_left) / float(expression_right)
        except:
            print "Unable to calculate an answer"

        # calculator provides answer
        if answer:
            self._text_to_speech("The answer is {}".format(answer))
