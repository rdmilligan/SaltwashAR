from rocky_robot_frames import *
from sporty_robot_frames import *

class Robot:

    def __init__(self):
        self.body_frame = None
        self.head_passive_frames = None
        self.head_speaking_frames = None
        self.head_frame_index = 0
        self.is_detected = False

    # get next frame
    def next_frame(self, is_speaking):
        glCallList(self.body_frame)

        self.head_frame_index += 1

        if is_speaking:

            if self.head_frame_index >= len(self.head_speaking_frames):
                self.head_frame_index = 0

            glCallList(self.head_speaking_frames[self.head_frame_index])

        else:

            if self.head_frame_index >= len(self.head_passive_frames):
                self.head_frame_index = 0

            glCallList(self.head_passive_frames[self.head_frame_index])

class RockyRobot(Robot):
 
    # load frames
    def load_frames(self, is_animated):
        self.body_frame = rocky_robot_body_frame()
        self.head_passive_frames = rocky_robot_head_passive_frames(is_animated)
        self.head_speaking_frames = rocky_robot_head_speaking_frames(is_animated)

class SportyRobot(Robot):
 
    # load frames
    def load_frames(self, is_animated):
        self.body_frame = sporty_robot_body_frame()
        self.head_passive_frames = sporty_robot_head_passive_frames(is_animated)
        self.head_speaking_frames = sporty_robot_head_speaking_frames(is_animated)
        
        
        
