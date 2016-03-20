# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from OpenGL.GL import *

gl_list_pyramid = None
gl_list_cube = None

def draw_pyramid(rotation):
    global gl_list_pyramid

    glTranslatef(0.0,0.0,-8.0)
    glRotatef(rotation,0.5,1.0,0.0) 

    if not gl_list_pyramid:
        gl_list_pyramid = glGenLists(1)
        glNewList(gl_list_pyramid, GL_COMPILE) 

        glBegin(GL_TRIANGLES)
        glColor3f(1.0,0.0,0.0)
        glVertex3f(0.0,1.0,0.0)
        glColor3f(0.0,1.0,0.0)
        glVertex3f(-1.0,-1.0,1.0)
        glColor3f(0.0,0.0,1.0)
        glVertex3f(1.0,-1.0,1.0)

        glColor3f(1.0,0.0,0.0)
        glVertex3f(0.0,1.0,0.0)
        glColor3f(0.0,0.0,1.0)
        glVertex3f(1.0,-1.0,1.0)
        glColor3f(0.0,1.0,0.0)
        glVertex3f(1.0,-1.0,-1.0)

        glColor3f(1.0,0.0,0.0)
        glVertex3f(0.0,1.0,0.0)
        glColor3f(0.0,1.0,0.0)
        glVertex3f(1.0,-1.0,-1.0)
        glColor3f(0.0,0.0,1.0)
        glVertex3f(-1.0,-1.0,-1.0)

        glColor3f(1.0,0.0,0.0)
        glVertex3f(0.0,1.0,0.0)
        glColor3f(0.0,0.0,1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glColor3f(0.0,1.0,0.0)
        glVertex3f(-1.0,-1.0,1.0)
        glEnd()

        glColor3f (1.0, 1.0, 1.0)
        glEndList()

    glCallList(gl_list_pyramid)

def draw_cube(rotation):
    global gl_list_cube

    glTranslatef(0.0,0.0,-9.0)    
    glRotatef(rotation,0.5,1.0,0.0)   

    if not gl_list_cube:
        gl_list_cube = glGenLists(1)
        glNewList(gl_list_cube, GL_COMPILE) 
             
        glBegin(GL_QUADS)
        glColor3f(0.0,1.0,0.0)
        glVertex3f(1.0,1.0,-1.0)
        glVertex3f(-1.0,1.0,-1.0)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(1.0,1.0,1.0)

        glColor3f(1.0,0.5,0.0)
        glVertex3f(1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(1.0,-1.0,-1.0)

        glColor3f(1.0,0.0,0.0)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(1.0,-1.0,1.0)

        glColor3f(1.0,1.0,0.0)
        glVertex3f(1.0,-1.0,-1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0,1.0,-1.0)
        glVertex3f(1.0,1.0,-1.0)

        glColor3f(0.0,0.0,1.0)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(-1.0,1.0,-1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0,-1.0,1.0)

        glColor3f(1.0,0.0,1.0)
        glVertex3f(1.0,1.0,-1.0)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(1.0,-1.0,1.0)
        glVertex3f(1.0,-1.0,-1.0)
        glEnd()

        glColor3f (1.0, 1.0, 1.0)
        glEndList()

    glCallList(gl_list_cube)
