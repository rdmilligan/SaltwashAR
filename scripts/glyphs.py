import cv2
from glyphfunctions import *
from glyphdatabase import *

class Glyphs:
    
    QUADRILATERAL_POINTS = 4
    BLACK_THRESHOLD = 100
    WHITE_THRESHOLD = 155
    GLYPH_NAME_INDEX = 3

    def __init__(self):
        with np.load('calibration/webcam_calibration_ouput.npz') as X:
            self.mtx, self.dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

    def detect(self, image):

        glyphs = []

        # Stage 1: Detect edges in image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        edges = cv2.Canny(gray, 100, 200)

        # Stage 2: Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        for contour in contours:

            # Stage 3: Shape check
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01*perimeter, True)

            if len(approx) == self.QUADRILATERAL_POINTS:

                # Stage 4: Perspective warping
                topdown_quad = get_topdown_quad(gray, approx.reshape(4, 2))

                # Stage 5: Border check
                if topdown_quad[(topdown_quad.shape[0]/100.0)*5, 
                                (topdown_quad.shape[1]/100.0)*5] > self.BLACK_THRESHOLD: continue

                # Stage 6: Get glyph pattern
                glyph_pattern = None
                
                try:
                    glyph_pattern = get_glyph_pattern(topdown_quad, self.BLACK_THRESHOLD, self.WHITE_THRESHOLD)
                except Exception as ex:
                    print(ex)
                
                if not glyph_pattern: continue

                 # Stage 7: Match glyph pattern
                glyph_found, glyph_rotation, glyph_name = match_glyph_pattern(glyph_pattern)

                if glyph_found:

                    # Stage 8: Duplicate glyph check
                    if glyph_name in [glyph[self.GLYPH_NAME_INDEX] for glyph in glyphs]: continue

                    # Stage 9: Get rotation and translation vectors
                    rvecs, tvecs = get_vectors(image, approx.reshape(4, 2), self.mtx, self.dist)
                    glyphs.append([rvecs, tvecs, glyph_rotation, glyph_name])

        return glyphs

