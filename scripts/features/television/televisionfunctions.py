# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

import cv2
import numpy as np

def _order_points(points):

    s = points.sum(axis=1)
    diff = np.diff(points, axis=1)
    
    ordered_points = np.zeros((4,2), dtype='float32')

    ordered_points[0] = points[np.argmin(s)]
    ordered_points[2] = points[np.argmax(s)]
    ordered_points[1] = points[np.argmin(diff)]
    ordered_points[3] = points[np.argmax(diff)]

    return ordered_points

def _max_width_height(points):

    (tl, tr, br, bl) = points

    top_width = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    bottom_width = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    max_width = max(int(top_width), int(bottom_width))

    left_height = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    right_height = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    max_height = max(int(left_height), int(right_height))

    return (max_width, max_height)

def _topdown_points(max_width, max_height):
    return np.array([
        [0, 0],
        [max_width-1, 0],
        [max_width-1, max_height-1],
        [0, max_height-1]], dtype='float32')

def get_topdown_quad(image, src):

    # src and dst points
    src = _order_points(src)

    (max_width,max_height) = _max_width_height(src)
    dst = _topdown_points(max_width, max_height)
 
    # warp perspective
    matrix = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(image, matrix, _max_width_height(src))

    return warped

def get_marker_pattern(image, black_threshold, white_threshold):

    # collect pixel from each cell (left to right, top to bottom)
    cells = []
    
    cell_half_width = int(round(image.shape[1] / 10.0))
    cell_half_height = int(round(image.shape[0] / 10.0))

    row1 = cell_half_height*3
    row2 = cell_half_height*5
    row3 = cell_half_height*7
    col1 = cell_half_width*3
    col2 = cell_half_width*5
    col3 = cell_half_width*7

    cells.append(image[row1, col1])
    cells.append(image[row1, col2])
    cells.append(image[row1, col3])
    cells.append(image[row2, col1])
    cells.append(image[row2, col2])
    cells.append(image[row2, col3])
    cells.append(image[row3, col1])
    cells.append(image[row3, col2])
    cells.append(image[row3, col3])

    # threshold pixels to either black or white
    for idx, val in enumerate(cells):
        if val < black_threshold:
            cells[idx] = 0
        elif val > white_threshold:
            cells[idx] = 1
        else:
            return None

    return cells

def add_substitute_quad(image, substitute_quad, dst):
 
    # dst (zeroed) and src points
    dst = _order_points(dst)
 
    (tl, tr, br, bl) = dst
    min_x = min(int(tl[0]), int(bl[0]))
    min_y = min(int(tl[1]), int(tr[1]))
 
    for point in dst:
        point[0] = point[0] - min_x
        point[1] = point[1] - min_y
 
    (max_width,max_height) = _max_width_height(dst)
    src = _topdown_points(max_width, max_height)
 
    # warp perspective (with white border)
    substitute_quad = cv2.resize(substitute_quad, (max_width,max_height))
 
    warped = np.zeros((max_height,max_width,3), np.uint8)
    warped[:,:,:] = 255
 
    matrix = cv2.getPerspectiveTransform(src, dst)
    cv2.warpPerspective(substitute_quad, matrix, (max_width,max_height), warped, borderMode=cv2.BORDER_TRANSPARENT)
 
    # add substitute quad
    image[min_y:min_y + max_height, min_x:min_x + max_width] = warped
 
    return image
 