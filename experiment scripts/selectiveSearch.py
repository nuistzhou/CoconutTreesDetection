#!/usr/bin/env python
'''
Usage:
    ./ssearch.py input_image (f|q)
    f=fast, q=quality
Use "l" to display less rects, 'm' to display more rects, "q" to quit.
'''
import cv2

def ssearch(img, para):
# if __name__ == '__main__':
    # If image path and f/q is not passed as command
    # line arguments, quit and display help message
    # if len(sys.argv) < 3:
    #     print(__doc__)
    #     sys.exit(1)
    proposals = list()

    # speed-up using multithreads
    cv2.setUseOptimized(True)
    cv2.setNumThreads(4)

    # read image
    im = cv2.imread(img)
    # resize image
    newHeight = 200
    newWidth = int(im.shape[1] * 200 / im.shape[0])
    # im = cv2.resize(im, (newWidth, newHeight))


    numShowRects = 150

# create Selective Search Segmentation Object using default parameters
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

    # set input image on which we will run segmentation
    ss.setBaseImage(im)

    # Switch to fast but low recall Selective Search method
    if (para == 'f'):
        ss.switchToSelectiveSearchFast()

    # Switch to high recall but slow Selective Search method
    elif (para == 'q'):
        ss.switchToSelectiveSearchQuality()

    # run selective search segmentation on input image
    rects = ss.process()
    print('Total Number of Region Proposals: {}'.format(len(rects)))


    imOut = im.copy()
    for i, rect in enumerate(rects):
        if (i < numShowRects):
            x, y, w, h = rect
            proposals.append((x, y, w, h))
            cv2.rectangle(imOut, (x, y), (x + w, y + h), (0, 0, 255), 1, cv2.LINE_AA)

    print "SSearch finished!"

    cv2.imwrite("/Users/ping/Downloads/chop_0_ssearch.png", imOut)


if __name__ == "__main__":
    ssearch("/Users/ping/Downloads/chop_0.png", 'f')