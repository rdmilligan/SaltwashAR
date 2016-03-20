# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

import speech_recognition as sr
from scipy.io import wavfile
import numpy as np

AUDIO_CLASSES = ['yes','no']
THRESHOLD_DIVISION = 4
NUMBER_OF_SLICES = 8
WAV_FILE = 'scripts/features/audioclassifier/word.wav'
DATA_FILE = 'scripts/features/audioclassifier/data.txt'

# get neural network target data
def _get_target(recognizer, audio):
    target = None
    text = None

    # use Google Speech Recognition to resolve audio to Yes or No
    try:
        text = recognizer.recognize_google(audio).lower()
        print text
    except sr.UnknownValueError:
        print "Google Speech Recognition could not understand audio"
    except sr.RequestError:
        print "Could not request results from Google Speech Recognition service"

    if not text: return

    # obtain target data i.e. 0 for Yes, 1 for No
    try:
        target = AUDIO_CLASSES.index(text)
    except ValueError:
        return

    return target

# get neural network input data
def _get_input():
    
    # load audio data (wav format)
    rate, data = wavfile.read(WAV_FILE)
    data = data / (2.**15)

    # get start and end position of word (word will be either Yes or No)
    thresold_level = np.amax(data) / THRESHOLD_DIVISION
    print "Thresold level: {}".format(thresold_level)

    start_pos = 0
    end_pos = 0
    
    prev_val = 0
    for idx, val in enumerate(data):
            
        if start_pos == 0 and val >= thresold_level:
            start_pos = idx
            
        if prev_val >= thresold_level and val < thresold_level:
            end_pos = idx

        prev_val = val

    print "Start position: {}".format(start_pos)
    print "End position: {}".format(end_pos)

    # get top peak in each slice
    slice_size = (end_pos - start_pos) / NUMBER_OF_SLICES
    print "Slice size: {}".format(slice_size)

    top_peaks = []

    for i in range(NUMBER_OF_SLICES):
        end_pos = start_pos + slice_size

        slice = data[start_pos:end_pos]
        top_peaks.append(np.amax(slice))

        start_pos = end_pos

    print "Top peaks: {}".format(top_peaks)

    # obtain input data as percentages e.g. [47, 100, 74, 70, 32, 16, 35, 41]
    # top peak in each slice will be a percentage of overall top peak
    input = []
    overall_top_peak = np.amax(top_peaks)

    for val in top_peaks:
        input_item = int((val / overall_top_peak) * 100)
        input.append(input_item)
     
    print "Input: {}".format(input)

    return input

# create neural network data
def create_data(text_to_speech):

    # ask user to say the word Yes or No
    text_to_speech("Say the word Yes or No")

    # save spoken word as wav data
    recognizer = sr.Recognizer()   
    
    with sr.Microphone() as source:
        print "listening..."
        audio = recognizer.listen(source)

    with open(WAV_FILE, "wb") as f:
        f.write(audio.get_wav_data())

    # get target data (and bail out if not Yes or No)
    target = _get_target(recognizer, audio)
    if target == None: return (None,None)

    # get input data
    input = _get_input()

    return (input,target)

# save input and target data
def save_data(input, target):
    if input == None or target == None: return

    with open(DATA_FILE, "a") as f:
        f.write(str(input) + '[{}]'.format(target) + '\n')

# load all input and target data
def load_data():
    inputs = []
    targets = []

    with open(DATA_FILE) as f:
        lines = f.readlines()

    for line in lines:

        line_parts = line.rstrip('\n').split('][')

        input = map(int, line_parts[0][1:].split(','))
        target = int(line_parts[1][:1])

        inputs.append(input)
        targets.append(target)

    return (inputs,targets)

    
