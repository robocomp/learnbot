from __future__ import print_function
import cv2
import numpy as np
import visual_auxiliary as va


def is_there_face(lbot, params=None, verbose=False):
    frame = lbot.getImage()
    mat = va.detect_face(frame)
    for row in mat:
        for cell in row:
            if cell == 1:
                return True
    return False