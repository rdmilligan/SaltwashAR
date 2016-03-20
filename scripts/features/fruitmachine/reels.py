# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

import random
import cv2
from OpenGL.GL import *
import PIL.Image

# global variables
patterns = [{'current_rotation': 0, 'total_rotation': 360, 'speed': 4 },
            {'current_rotation': 0, 'total_rotation': 450, 'speed': 3 },
            {'current_rotation': 0, 'total_rotation': 540, 'speed': 5 },
            {'current_rotation': 0, 'total_rotation': 630, 'speed': 6 }]

gl_list_reel = None

# give each reel a new pattern (unless it is being held)
def refresh_reels(reels, holds):
    global patterns

    for i, reel in enumerate(reels):
        if reel and (i in holds): continue

        new_reel = random.choice(patterns).copy()

        if reel:
            new_reel['current_rotation'] = reel['current_rotation'] % 360
            new_reel['total_rotation'] += new_reel['current_rotation']

        reels[i] = new_reel

    return reels

# spin the reels
def rotate_reels(reels):

    for i, reel in enumerate(reels):

        if not reel or (reel['current_rotation'] == reel['total_rotation']): continue

        next_rotation = reel['current_rotation'] + reel['speed']

        if next_rotation >= reel['total_rotation']:
            reels[i]['current_rotation'] = reel['total_rotation']
        else:
            reels[i]['current_rotation'] = next_rotation

    return reels

# check whether any of the reels are still spinning
def is_reels_rotating(reels):

    is_rotating = False    

    for reel in reels:
        if reel['current_rotation'] != reel['total_rotation']:
            is_rotating = True
            break

    return is_rotating

# if all reels match then player has won
def is_reels_win(reels):

    end_rotations = []

    for reel in reels:
        end_rotations.append(reel['total_rotation'] % 360)

    return all(i == end_rotations[0] for i in end_rotations)

# draw the hold bars above the reels
def draw_holds(holds, image):
    
    for hold in holds:
        if hold == None: continue

        if hold == 0:
            cv2.line(image, (120,300), (200,300), (0,255,0), 2)
        elif hold == 1:
            cv2.line(image, (280,300), (360,300), (0,255,0), 2)
        elif hold == 2:
            cv2.line(image, (440,300), (520,300), (0,255,0), 2)

    return image

# draw the reels of a fruit machine
def draw_reels(reels):
    global gl_list_reel

    if not gl_list_reel:
        _load_reel()

    previous_rotation = 0
    translate_x = -1.5
    translate_y = -1.2
    translate_z = -7.0

    for reel in reels:
        if not reel: continue

        rotation = reel['current_rotation'] - previous_rotation
        previous_rotation += rotation

        glTranslatef(translate_x,translate_y,translate_z) 
        glRotatef(rotation,1.0,0.0,0.0)
        glCallList(gl_list_reel)
    
        translate_x = 1.5
        translate_y = 0.0
        translate_z = 0.0        

# load reel into a gl display list
def _load_reel():
    global gl_list_reel

    # obtain pics of apple, cherries, orange, watermelon
    materials = {}

    MATERIALS_PATH = 'scripts/features/fruitmachine/'

    image = PIL.Image.open('{}apple.jpg'.format(MATERIALS_PATH))
    image = image.tobytes('raw', 'RGBX', 0, -1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 100, 100, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    materials['material_apple'] = texture_id

    image = PIL.Image.open('{}cherries.jpg'.format(MATERIALS_PATH))
    image = image.tobytes('raw', 'RGBX', 0, -1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 100, 100, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    materials['material_cherries'] = texture_id

    image = PIL.Image.open('{}orange.jpg'.format(MATERIALS_PATH))
    image = image.tobytes('raw', 'RGBX', 0, -1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 100, 100, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    materials['material_orange'] = texture_id

    image = PIL.Image.open('{}watermelon.jpg'.format(MATERIALS_PATH))
    image = image.tobytes('raw', 'RGBX', 0, -1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 100, 100, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    materials['material_watermelon'] = texture_id

    # generate gl diplay list
    gl_list_reel = glGenLists(1)
    glNewList(gl_list_reel, GL_COMPILE) 

    glBindTexture(GL_TEXTURE_2D, materials['material_apple'])
    glBegin(GL_POLYGON)
    glTexCoord2f(1.0,1.0)       
    glVertex3f(0.5,0.5,-0.5)
    glTexCoord2f(0.0,1.0)
    glVertex3f(-0.5,0.5,-0.5)
    glTexCoord2f(0.0,0.0)
    glVertex3f(-0.5,0.5,0.5)
    glTexCoord2f(1.0,0.0)
    glVertex3f(0.5,0.5,0.5)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, materials['material_cherries'])
    glBegin(GL_POLYGON)
    glTexCoord2f(1.0,1.0)
    glVertex3f(0.5,-0.5,0.5)
    glTexCoord2f(0.0,1.0)
    glVertex3f(-0.5,-0.5,0.5)
    glTexCoord2f(0.0,0.0)
    glVertex3f(-0.5,-0.5,-0.5)
    glTexCoord2f(1.0,0.0)
    glVertex3f(0.5,-0.5,-0.5)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, materials['material_orange'])
    glBegin(GL_POLYGON)
    glTexCoord2f(1.0,1.0)
    glVertex3f(0.5,0.5,0.5)
    glTexCoord2f(0.0,1.0)
    glVertex3f(-0.5,0.5,0.5)
    glTexCoord2f(0.0,0.0)
    glVertex3f(-0.5,-0.5,0.5)
    glTexCoord2f(1.0,0.0)
    glVertex3f(0.5,-0.5,0.5)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, materials['material_watermelon'])
    glBegin(GL_POLYGON)
    glTexCoord2f(1.0,1.0)
    glVertex3f(0.5,-0.5,-0.5)
    glTexCoord2f(0.0,1.0)
    glVertex3f(-0.5,-0.5,-0.5)
    glTexCoord2f(0.0,0.0)
    glVertex3f(-0.5,0.5,-0.5)
    glTexCoord2f(1.0,0.0)
    glVertex3f(0.5,0.5,-0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(-0.5,0.5,0.5)
    glVertex3f(-0.5,0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(0.5,0.5,-0.5)
    glVertex3f(0.5,0.5,0.5)
    glVertex3f(0.5,-0.5,0.5)
    glVertex3f(0.5,-0.5,-0.5)
    glEnd()

    glEndList()