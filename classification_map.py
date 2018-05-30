import numpy as np
from config import Parameters
from PIL import Image

test_labels = np.load('/Users/ping/Documents/thesis/data/result/test_labels.npy')
predicted_probs = np.load("/Users/ping/Documents/thesis/data/result/predicted_probs.npy")
dim_y = 1773
dim_x = 5310
classification_image = np.zeros((dim_y, dim_x), dtype = np.uint8)
classification_map_sumup = np.zeros((dim_y, dim_x), dtype = np.uint8)
predicted_probs_matrix = np.zeros((dim_y, dim_x), dtype = np.float)
window_top_left_y = 0
window_bottom_right_y = 90
counter = 0
counterCoco = 0
print Parameters.strideSize

while window_bottom_right_y < dim_y - Parameters.samplePatchSize:
    window_bottom_right_x = 90
    window_top_left_x = 0
    while (window_bottom_right_x < dim_x - Parameters.samplePatchSize):
        if test_labels[counter] == 1:
            classification_image[window_top_left_y: window_bottom_right_y,
                          window_top_left_x: window_bottom_right_x] = 255
            classification_map_sumup[window_top_left_y: window_bottom_right_y,\
                          window_top_left_x: window_bottom_right_x] += 1
            predicted_probs_matrix[window_top_left_y: window_bottom_right_y,\
                          window_top_left_x: window_bottom_right_x] += predicted_probs[counter, 1]
            counterCoco += 1
        counter += 1
        window_top_left_x += Parameters.strideSize
        window_bottom_right_x += Parameters.strideSize
    window_top_left_y += Parameters.strideSize
    window_bottom_right_y += Parameters.strideSize

print "Number of {0} coconut trees detected from {1} windows, with a percentage of " \
      "{2: .2f}%!".format(counterCoco, counter, float(counterCoco)/counter * 100)

predicted_probs_matrix_max = np.max(predicted_probs_matrix)
predicted_probs_matrix = (predicted_probs_matrix/predicted_probs_matrix_max) * 255
predicted_probs_matrix = predicted_probs_matrix.astype(np.uint8)
img_summed_up_predicted_probs = Image.fromarray(predicted_probs_matrix)
img_summed_up_predicted_probs.save("/Users/ping/thesis/data/result/classification_map_summed_up_probs.png")


print np.min(classification_map_sumup)
print np.max(classification_map_sumup)
img = Image.fromarray(classification_image)
img_summed_up = Image.fromarray(classification_map_sumup)
img.save("/Users/ping/thesis/data/result/classification_map.png")
img_summed_up.save("/Users/ping/thesis/data/result/classification_map_summed_up.png")
