import numpy as np
from config import Parameters
from PIL import Image

test_labels = np.load('/Users/ping/thesis/data/result/test_labels.npy')
dim_y = 1773
dim_x = 5310
classification_image = np.zeros((1773, 5310), dtype = np.uint8)
window_top_left_y = 0
window_bottom_right_y = 90
counter = 0

print Parameters.strideSize

while window_bottom_right_y < dim_y - Parameters.samplePatchSize:
    window_bottom_right_x = 90
    window_top_left_x = 0
    while (window_bottom_right_x < dim_x - Parameters.samplePatchSize):
        if test_labels[counter] == 1:
            classification_image[window_top_left_y: window_bottom_right_y,
                          window_top_left_x: window_bottom_right_x] = 255

        print "The {0}th window!".format(counter)
        counter += 1
        window_top_left_x += Parameters.strideSize
        window_bottom_right_x += Parameters.strideSize
    window_top_left_y += Parameters.strideSize
    window_bottom_right_y += Parameters.strideSize

img = Image.fromarray(classification_image)
img.save("/Users/ping/thesis/data/result/classification_map.png")
