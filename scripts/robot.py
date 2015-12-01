from rocky_robot_frames import *
from sporty_robot_frames import *

class Robot:

    def __init__(self):
        self.body_frame = None
        self.head_frames = []
        self.head_frames_length = 0
        self.head_frame_index = 0
        self.is_detected = False

    # get next frame
    def next_frame(self):
        self.head_frame_index += 1

        if self.head_frame_index >= self.head_frames_length:
            self.head_frame_index = 0

        glCallList(self.body_frame)
        glCallList(self.head_frames[self.head_frame_index])

class RockyRobot(Robot):
 
    # load frames
    def load_frames(self, animation):
        self.body_frame = rocky_robot_body_frame()
        self.head_frames = rocky_robot_head_frames(animation)
        self.head_frames_length = len(self.head_frames)

class SportyRobot(Robot):
 
    # load frames
    def load_frames(self, animation):
        self.body_frame = sporty_robot_body_frame()
        self.head_frames = sporty_robot_head_frames(animation)
        self.head_frames_length = len(self.head_frames)

        
        
        
