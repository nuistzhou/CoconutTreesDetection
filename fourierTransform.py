import time
import numpy as np
import cv2

start = time.time()
print("Processing...")
img = cv2.imread("/Users/ping/Documents/thesis/data/rgb_image_ssearch/rgb_image_ssearch.tif")
f_img = np.fft.fft2(img, axes = (0, 1))
try:
    np.save("/Users/ping/Documents/thesis/data/rgb_image_ssearch/fourierTransform.npy", f_img)
except:
    pass

end = time.time()
print(end - start)
print ("Finished!")