import numpy as np
import cv2

def cropImage(filename):
    ## Load image
    image_raw = cv2.imread(filename)
    width, height, bands = image_raw.shape
