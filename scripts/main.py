from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from PIL import Image
import numpy as np
from robot import Robot
from webcam import Webcam
from glyphs import Glyphs
from browser import Browser
from configprovider import ConfigProvider
from constants import *

class SaltwashAR:
 
    # constants
    INVERSE_MATRIX = np.array([[ 1.0, 1.0, 1.0, 1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [ 1.0, 1.0, 1.0, 1.0]])

    def __init__(self):
        # initialise robots
        self.rocky_robot = Robot()
        self.sporty_robot = Robot()

        # initialise webcam
        self.webcam = Webcam()

        # initialise glyphs
        self.glyphs = Glyphs()
        self.glyphs_cache = None

        # initialise browser
        self.browser = Browser()
        
        # initialise config
        self.config_provider = ConfigProvider()

        # initialise texture
        self.texture_background = None

    def _init_gl(self, Width, Height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(33.7, 1.3, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
        # load robots
        self.rocky_robot.load('rocky_robot', self.config_provider.animation)
        self.sporty_robot.load('sporty_robot', self.config_provider.animation)
        
        # start threads
        self.webcam.start()
        self.browser.start()

        # assign texture
        glEnable(GL_TEXTURE_2D)
        self.texture_background = glGenTextures(1)

    def _draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # reset robots
        self.rocky_robot.is_detected = False
        self.sporty_robot.is_detected = False

        # get image from webcam
        image = self.webcam.get_current_frame()

        # handle background
        self._handle_background(image)

        # handle glyphs
        self._handle_glyphs(image)
       
        # handle browser
        self._handle_browser()

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
            
            rvecs, tvecs, _, glyph_name = glyph

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
                self.rocky_robot.is_detected = True
                glCallList(self.rocky_robot.next_frame())
            elif glyph_name == SPORTY_ROBOT:
                self.sporty_robot.is_detected = True
                glCallList(self.sporty_robot.next_frame())
            
            glColor3f(1.0, 1.0, 1.0)
            glPopMatrix()

    def _handle_browser(self):

        # check browser enabled
        if not self.config_provider.browser: return

        # handle browser
        if self.rocky_robot.is_detected:
            self.browser.load(ROCK)
        elif self.sporty_robot.is_detected:
            self.browser.load(SPORT)
        else:
            self.browser.halt()

    def main(self):
        # setup and run OpenGL
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(800, 400)
        self.window_id = glutCreateWindow("SaltwashAR")
        glutDisplayFunc(self._draw_scene)
        glutIdleFunc(self._draw_scene)
        self._init_gl(640, 480)
        glutMainLoop()
 
# run an instance of SaltwashAR
saltwashAR = SaltwashAR()
saltwashAR.main()
