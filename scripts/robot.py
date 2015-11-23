import os, glob
from objloader import *

class Robot:

    def __init__(self):
        self.frames = []
        self.frames_length = 0
        self.frame_index = 0
        self.is_detected = False

    # load frames from directory
    def load(self, directory, animation):
        os.chdir(directory)
        
        for file in glob.glob("*.obj"):
            self.frames.append(OBJ(file))
            if not animation: break 

        os.chdir('..')
        self.frames_length = len(self.frames)

    # get next frame
    def next_frame(self):
        self.frame_index += 1

        if self.frame_index >= self.frames_length:
            self.frame_index = 0

        return self.frames[self.frame_index].gl_list

        
        
        
