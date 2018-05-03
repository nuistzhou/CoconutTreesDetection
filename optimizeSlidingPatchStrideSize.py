from __future__ import division
from math import sqrt

def calNonOverlapPercent(strideSize):
    beyondThresholdCounter = 0
    distanceThreshold = 12
    for x in range(strideSize):
        for y in range(strideSize):
            distanceTopLeft = sqrt(x**2 + y**2)
            distanceTopRight = sqrt((x - strideSize - 1)**2 + y**2)
            distanceBottomLeft = sqrt(x**2 + (y - strideSize - 1)**2)
            distanceBottomRight = sqrt((x - strideSize - 1)**2 + (y - strideSize -1)**2)
            minDistance = min(distanceTopLeft, distanceTopRight, distanceBottomLeft, distanceBottomRight)
            if minDistance >= distanceThreshold:
                beyondThresholdCounter += 1
    nonOverlapPercent = beyondThresholdCounter/strideSize**2 *100
    return nonOverlapPercent

NrPixelsX = 17761
NrPixelsY = 25006
# From 5 pixels to 45 pixels(half patch size)
print "Stride Size      ", "Recall"
for strideSize in range(5,50,5):
    nonOverlapPercent = calNonOverlapPercent(strideSize)
    print("%.2f" % (100 - nonOverlapPercent))


