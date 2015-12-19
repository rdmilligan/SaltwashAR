from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from PIL import Image
import numpy as np
from configprovider import ConfigProvider
from robot import *
from webcam import Webcam
from glyphs import Glyphs
from features import Features
from constants import *

class SaltwashAR:
 
    # constants
    INVERSE_MATRIX = np.array([[ 1.0, 1.0, 1.0, 1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [ 1.0, 1.0, 1.0, 1.0]])

    def __init__(self):
        # initialise config
        self.config_provider = ConfigProvider()

        # initialise robots
        self.rocky_robot = RockyRobot()
        self.sporty_robot = SportyRobot()

        # initialise webcam
        self.webcam = Webcam()

        # initialise glyphs
        self.glyphs = Glyphs()
        self.glyphs_cache = None

        # initialise features
        self.features = Features(self.config_provider)

        # initialise texture
        self.texture_background = None

    def _init_gl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(33.7, 1.3, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        # load robots frames
        self.rocky_robot.load_frames(self.config_provider.animation)
        self.sporty_robot.load_frames(self.config_provider.animation)

        # start webcam thread
        self.webcam.start()

        # assign texture
        glEnable(GL_TEXTURE_2D)
        self.texture_background = glGenTextures(1)

    def _draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # reset robots
        self.rocky_robot.is_facing = False
        self.sporty_robot.is_facing = False

        # get image from webcam
        image = self.webcam.get_current_frame()

        # handle background
        self._handle_background(image)

        # handle glyphs
        self._handle_glyphs(image)
       
        # handle features
        self.features.handle(self.rocky_robot.is_facing, self.sporty_robot.is_facing, image)

        glutSwapBuffers()

    def _handle_background(self, image):
        
        # convert image to OpenGL texture format
        bg_image = cv2.flip(image, 0)
        bg_image = Image.fromarray(bg_image)     
        ix = bg_image.size[0]
        iy = bg_image.size[1]
        bg_image = bg_image.tostring("raw", "BGRX", 0, -1)
 
        # create background texture
        glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
        
        # draw background
        glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glPushMatrix()
        glTranslatef(0.0,0.0,-10.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 0.0)
        glEnd( )
        glPopMatrix()

    def _handle_glyphs(self, image):

        # attempt to detect glyphs
        glyphs = []

        try:
            glyphs = self.glyphs.detect(image)
        except Exception as ex:
            print(ex)

        # manage glyphs cache
        if glyphs:
            self.glyphs_cache = glyphs
        elif self.glyphs_cache: 
            glyphs = self.glyphs_cache
            self.glyphs_cache = None
        else:
            return

        for glyph in glyphs:
            
            rvecs, tvecs, glyph_rotation, glyph_name = glyph

            # build view matrix
            rmtx = cv2.Rodrigues(rvecs)[0]

            view_matrix = np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0]],
                                    [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[1]],
                                    [rmtx[2][0],rmtx[2][1],rmtx[2][2],tvecs[2]],
                                    [0.0       ,0.0       ,0.0       ,1.0    ]])

            view_matrix = view_matrix * self.INVERSE_MATRIX

            view_matrix = np.transpose(view_matrix)

            # load view matrix and draw cube
            glPushMatrix()
            glLoadMatrixd(view_matrix)

            if glyph_name == ROCKY_ROBOT:
                self.rocky_robot.next_frame(glyph_rotation, self.features.is_speaking())
            elif glyph_name == SPORTY_ROBOT:
                self.sporty_robot.next_frame(glyph_rotation, self.features.is_speaking())

            glColor3f(1.0, 1.0, 1.0)
            glPopMatrix()

    def main(self):
        # setup and run OpenGL
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(800, 400)
        self.window_id = glutCreateWindow("SaltwashAR")
        glutDisplayFunc(self._draw_scene)
        glutIdleFunc(self._draw_scene)
        self._init_gl()
        glutMainLoop()
 
# run an instance of SaltwashAR
saltwashAR = SaltwashAR()
saltwashAR.main()
