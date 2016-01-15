# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from rockyrobotframes import *
from sportyrobotframes import *
from constants import *

class Robot:

    def __init__(self):
        self.body_frame = None
        self.head_passive_frames = None
        self.head_speaking_frames = None
        self.head_happy_frames = None
        self.head_sad_frames = None
        self.head_angry_frames = None
        self.degrees_90_frame = None
        self.degrees_180_frame = None
        self.degrees_270_frame = None
        self.head_frame_index = 0
        self.is_rendered = False
        self.is_facing = False

    # reset robot
    def reset(self):
        self.is_rendered = False
        self.is_facing = False

    # get next frame
    def next_frame(self, rotation, is_speaking, emotion):
        self.is_rendered = True
        
        # handle any rotation
        if rotation != 0:
            self.is_facing = False

            if rotation == 1:
                glCallList(self.degrees_90_frame)
            elif rotation == 2:
                glCallList(self.degrees_180_frame)
            elif rotation == 3:
                glCallList(self.degrees_270_frame)

            return
        
        # otherwise handle facing robot
        self.is_facing = True
        glCallList(self.body_frame)

        if is_speaking:
            self._render_head(self.head_speaking_frames)

        elif emotion == HAPPY:
            self._render_head(self.head_happy_frames)

        elif emotion == SAD:
            self._render_head(self.head_sad_frames)

        elif emotion == ANGRY:
            self._render_head(self.head_angry_frames)

        else:
            self._render_head(self.head_passive_frames)

    # render the robot's head
    def _render_head(self, frames):
        self.head_frame_index += 1

        if self.head_frame_index >= len(frames):
            self.head_frame_index = 0

        glCallList(frames[self.head_frame_index])   

class RockyRobot(Robot):
 
    # load frames
    def load_frames(self, is_animated):
        self.body_frame = rocky_robot_body_frame()
        self.head_passive_frames = rocky_robot_head_passive_frames(is_animated)
        self.head_speaking_frames = rocky_robot_head_speaking_frames(is_animated)
        self.head_happy_frames = rocky_robot_head_happy_frames(is_animated)
        self.head_sad_frames = rocky_robot_head_sad_frames(is_animated)
        self.head_angry_frames = rocky_robot_head_angry_frames(is_animated)
        self.degrees_90_frame = rocky_robot_degrees_90_frame()
        self.degrees_180_frame = rocky_robot_degrees_180_frame()
        self.degrees_270_frame = rocky_robot_degrees_270_frame()

class SportyRobot(Robot):
 
    # load frames
    def load_frames(self, is_animated):
        self.body_frame = sporty_robot_body_frame()
        self.head_passive_frames = sporty_robot_head_passive_frames(is_animated)
        self.head_speaking_frames = sporty_robot_head_speaking_frames(is_animated)
        self.head_happy_frames = sporty_robot_head_happy_frames(is_animated)
        self.head_sad_frames = sporty_robot_head_sad_frames(is_animated)
        self.head_angry_frames = sporty_robot_head_angry_frames(is_animated)
        self.degrees_90_frame = sporty_robot_degrees_90_frame()
        self.degrees_180_frame = sporty_robot_degrees_180_frame()
        self.degrees_270_frame = sporty_robot_degrees_270_frame()