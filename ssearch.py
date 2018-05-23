#!/usr/bin/env python
'''
Usage:
    ./ssearch.py input_image (f|q)
    f=fast, q=quality
Use "l" to display less rects, 'm' to display more rects, "q" to quit.
'''
import os
import sys
import glob
import cv2
import numpy as np
from scipy.misc import imsave

def cropImage(filename, chopsize):
    image_raw = cv2.imread(filename)
    height, width, bands = image_raw.shape
    image_raw = np.transpose(image_raw, axes = (1,0,2))
    pixelAddX = width%chopsize
    pixelAddY = height%chopsize
    chopColNr = width/chopsize
    chopRowNr = height/chopsize

    if pixelAddX != 0:
        chopColNr += 1
    if pixelAddY != 0:
        chopRowNr += 1
    chopList = list()

    for j in range(chopRowNr):
        for i in range(chopColNr):
            tempArray = np.zeros((chopsize, chopsize, 3), dtype = np.uint8)
            # chop at the right bottom corner
            if i == chopColNr - 1 and j == chopRowNr -1:
                chopArray = image_raw[i * chopsize: (i * chopsize + pixelAddX),
                            j * chopsize: (j * chopsize + pixelAddY), :]
                tempArray[:pixelAddX, :pixelAddY, :] = chopArray
            # chop at the right edge
            elif i == chopColNr -1:
                chopArray = image_raw[i * chopsize: (i * chopsize + pixelAddX),
                            j * chopsize: (j + 1) * chopsize, :]
                tempArray[:pixelAddX, :, :] = chopArray
            # chop at the bottom line
            elif j == chopRowNr -1:
                chopArray = image_raw[i * chopsize: (i + 1) * chopsize,
                            j * chopsize: (j * chopsize + pixelAddY), :]
                tempArray[:, :pixelAddY, :] = chopArray
            # normal chop does not need adding pixels
            else:
                tempArray[:, :, :] = image_raw[i * chopsize: (i + 1) * chopsize,
                                     j * chopsize: (j + 1) * chopsize, :
                                     ]
            chopList.append(tempArray)
    return chopList, chopColNr, chopRowNr

def ssearch(imageFilename, qOrf, j):
    # If image path and f/q is not passed as command
    # line arguments, quit and display help message

    # speed-up using multithreads
    cv2.setUseOptimized(True)
    cv2.setNumThreads(4)

    # read image
    im = cv2.imread(imageFilename)
    # resize image
    # newHeight = 200
    # newWidth = int(im.shape[1] * 200 / im.shape[0])
    # im = cv2.resize(im, (newWidth, newHeight))

    # create Selective Search Segmentation Object using default parameters
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

    # set input image on which we will run segmentation
    ss.setBaseImage(im)

    # Switch to fast but low recall Selective Search method
    if (qOrf == 'f'):
        ss.switchToSelectiveSearchFast()

    # Switch to high recall but slow Selective Search method
    elif (qOrf == 'q'):
        ss.switchToSelectiveSearchQuality()
    # if argument is neither f nor q print help message

    # run selective search segmentation on input image
    rects = ss.process()
    print('Total Number of Region Proposals: {}'.format(len(rects)))

    # number of region proposals to show
    numShowRects = 100
    # increment to increase/decrease total number
    # of reason proposals to be shown
    increment = 50

    # create a copy of original image
    imOut = im.copy()

    # itereate over all the region proposals
    for i, rect in enumerate(rects):
        # draw rectangle for region proposal till numShowRects
        # if (i < numShowRects):
        x, y, w, h = rect
        cv2.rectangle(imOut, (x, y), (x + w, y + h), (0, 255, 0), 1, cv2.LINE_AA)
        # else:
        #     break

    # show output
    # cv2.imshow("Output", imOut)
    cv2.imwrite("/Users/ping/Documents/thesis/data/ssearch_test/Proposal_{0}_chop_{1}.png".format(qOrf,j),imOut)
    print '{0} is finished!'.format(j)
# close image show window

if __name__ == "__main__":
    # chopArrayList = cropImage("/Users/ping/Documents/thesis/data/ssearch_test/rgb_image_clipped.tif", 1024)[0]
    # for i, chopArray in enumerate(chopArrayList):
    #     imsave("/Users/ping/Documents/thesis/data/ssearch_test/chop_{0}.png".format(i), chopArray)
    os.chdir("/Users/ping/Documents/thesis/data/ssearch_test")
    avgCocoNpyFilenames = glob.glob("chop_*.png")
    for i, imgFilename in enumerate(avgCocoNpyFilenames):
        ssearch(imgFilename,'f', i)
