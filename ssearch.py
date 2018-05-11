# -*- coding: utf-8 -*-
from __future__ import (
    division,
    print_function,
)

import selectivesearch
import cv2

def main(image):

    img = cv2.imread(image)
    # img = skimage.data.astronaut()

    print ("Detecting...")

    # perform selective search
    img_lbl, regions = selectivesearch.selective_search(
        img, scale=500, sigma=0.9, min_size=10)

    candidates = set() # Unordered collection of unique elements

    for r in regions:
        i = 0
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 2000 pixels
        # if r['size'] < 2000: ##Default value
        if r['size'] < 80:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        if w / h > 1.2 or h / w > 1.2:
            continue
        # candidates.add(r['rect'])
        candidates.add((x, y, w, h))
        i += 1
        print (i)

    print ("Finished detecting!")
    print ("Number of {0} proposals detected".format(len(candidates)))
    # draw rectangles on the original image
    # fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    # ax.imshow(img)
    for x, y, w, h in candidates:
        print(x, y, w, h)
        # rect = mpatches.Rectangle(
        #     (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        # ax.add_patch(rect)

    # plt.show()

if __name__ == "__main__":
    main("/Users/ping/Documents/thesis/data/rgb_image_ssearch/rgb_image_ssearch.tif")
    # main()