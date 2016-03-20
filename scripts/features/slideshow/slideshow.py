# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature, Speaking
import numpy as np
import os, glob
import cv2
from threading import Thread
from time import sleep

class Slideshow(Feature, Speaking):
 
    FEATURE_PATH = 'scripts/features/slideshow/'
    ROOT_PATH = '../../../'
    SLIDE_OFFSET = 50

    def __init__(self, text_to_speech):
        Feature.__init__(self)
        Speaking.__init__(self, text_to_speech)
        self.background_image = np.array([])
        self.slides = []
        self.blurbs = []
        self.current_item = 0
        self.current_slide = np.array([])
        self.blurb_thread = None
        self._get_slides_and_blurbs()

    def stop(self):
        Feature.stop(self)
        self.background_image = np.array([])

    # load slideshow
    def _get_slides_and_blurbs(self):
        os.chdir(self.FEATURE_PATH)

        for slide in glob.glob('*.jpg'):
            self.slides.append(slide)

        for blurb in glob.glob('*.txt'):
            self.blurbs.append(blurb)

        os.chdir(self.ROOT_PATH) 

        if len(self.slides) != len(self.blurbs):
            self.slides = []
            self.blurbs = []
            print "Unable to load slideshow as number of slides not equal to number of blurbs"
        elif not self.slides:
            print "Unable to load slideshow as no slides or blurbs found"

    # slideshow thread
    def _thread(self, args):
        image = args

        # check slides loaded
        if not self.slides: return

        # reset current item, if at end of slides
        if self.current_item >= len(self.slides): 
            self.current_item = 0

        # get next slide and blurb, if at end of current blurb
        if not self.blurb_thread or not self.blurb_thread.is_alive():
            self.current_slide = cv2.imread('{}{}'.format(self.FEATURE_PATH, self.slides[self.current_item]))

            with open('{}{}'.format(self.FEATURE_PATH, self.blurbs[self.current_item]), 'r') as blurb_file:
                blurb = blurb_file.readline()
            
            self.blurb_thread = Thread(target=self._blurb_thread, args=(blurb,))
            self.blurb_thread.start()           

        # update current background image with slide
        slide_offset_and_height = self.SLIDE_OFFSET + self.current_slide.shape[0]
        slide_offset_and_width = self.SLIDE_OFFSET + self.current_slide.shape[1]            

        if slide_offset_and_height <= image.shape[0] and slide_offset_and_width <= image.shape[1]:
            image[self.SLIDE_OFFSET:slide_offset_and_height, self.SLIDE_OFFSET:slide_offset_and_width] = self.current_slide
            self.background_image = image
        else:
            print "Unable to use slide as size larger than background image"
            self.background_image = np.array([])

    # blurb thread
    def _blurb_thread(self, blurb):
        if blurb: 
            self._text_to_speech(blurb)
        
        self.current_item += 1
        sleep(4)