import os
import time
import glob
import numpy as np
import cv2
from qgis.core import *
from PyQt4.QtCore import *
from PIL import Image
from skimage.feature import peak_local_max
from config import Parameters
import matplotlib.pyplot as plt
import imp, tools
imp.reload(tools)

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
            # normal chop does not need addingCoco pixels
            else:
                tempArray[:, :, :] = image_raw[i * chopsize: (i + 1) * chopsize,
                                     j * chopsize: (j + 1) * chopsize, :
                                     ]
            chopList.append(tempArray)
    return chopList, chopColNr, chopRowNr

def createImageFromCrops(chopsize, chopList, chopColNr, chopRowNr):
    array = np.zeros((chopsize * chopColNr, chopsize * chopRowNr, 3), dtype = np.uint8)
    counter = 0
    for j in range(chopRowNr):
        for i in range(chopColNr):
            array[i * chopsize: (i + 1) * chopsize, j * chopsize : (j + 1) * chopsize, :] = chopList[counter]
            counter += 1
    array_new = np.transpose(array, (1,0,2))
    img = Image.fromarray(array_new, 'RGB')
    img.save('/Users/ping/Documents/thesis/data/proposal_test/stiched.png')
    img.show()

def detectProposals(chopArrayList):
    """Return the array of proposal centers' pixel coordinates"""
    os.chdir(Parameters.resultPath)
    avgCocoNpyFilenames = glob.glob("avgCocotrees*enlarged.npy")
    f_avgCocoList = list()
    for avgCocoFilename in avgCocoNpyFilenames:
        avgCocoArray = np.load(avgCocoFilename)
        f_avgCoco = np.fft.fft2(np.fft.fftshift(avgCocoArray, axes=(0,1)), axes=(0, 1))
        f_avgCocoList.append(f_avgCoco)

    proposalCentersList = list()
    for chopArray in chopArrayList:
        f_chop = np.fft.fft2(chopArray, axes=(0, 1))
        f_inversedList = list()
        for f_avgCoco in f_avgCocoList:
            multiplication = np.multiply(f_avgCoco, f_chop)
            f_inversed = np.real(np.fft.ifft2(multiplication,axes=(0,1)))
            f_inversed = np.average(f_inversed,axis=2)
            f_inversedList.append(f_inversed)

        f_inversedArray = np.array(f_inversedList)
        # print "The dimension of the f_inversedArray is {0})".format(f_inversedArray.shape)
        f_inversedArrayStackMax = f_inversedArray.max(axis = 0)
        # distanceList = [1]
        # peak_localmax = list()
        # avgLocalPeak = np.zeros((90, 90), dtype=np.uint8)
        # for distance in distanceList[:1]:
        #     for f_inversed in f_inversedList:

        # distanceList = [1, 5, 10, 15]
        # localPeaksList = list()
        # for distance in distanceList:
        distance = 10
        f_inversedArrayStackLocalPeak = peak_local_max(f_inversedArrayStackMax, min_distance =distance, indices = True)
        # localPeaksList.append(f_inversedArrayStackLocalPeak)
        # Every chop has 4 lists based on different "min_distance" parameter specified above
        proposalCentersList.append(f_inversedArrayStackLocalPeak)


                # peak_localMax_temp = peak_local_max(f_inversed, min_distance =distance, indices = True)
                # peak_localMax_temp = peak_localMax_temp.tolist()
                # peak_localmax.extend(peak_localMax_temp)


        # peak_localmax = map(list, (set(map(tuple,peak_localmax))))
        # peak_localmax = peak_local_max(f_inversed, min_distance = i, indices = True)
        # peak_localmax_5 = peak_local_max(f_inversed, min_distance = 5, indices = True)
        # peak_localmax_10 = peak_local_max(f_inversed, min_distance = 10, indices = True)
        # peak_localmax_15 = peak_local_max(f_inversed, min_distance = 15, indices = True)

        # plt.figure(1), plt.imshow(f_inversed)
        # plt.figure(2)
        #
        # plt.subplot(2, 2, 1), plt.imshow(chopArray), \
        # plt.plot(peak_localmax[:, 1], peak_localmax[:, 0], 'r+'), plt.title("Minimum peaks distance Not set")
        # plt.subplot(2, 2, 2), plt.imshow(chopArray), \
        # plt.plot(peak_localmax_5[:, 1], peak_localmax_5[:, 0], 'r+'), plt.title("Minimum peaks distance = 5 pixels")
        # plt.subplot(2, 2, 3), plt.imshow(chopArray), \
        # plt.plot(peak_localmax_10[:, 1], peak_localmax_10[:, 0], 'r+'),plt.title("Minimum peaks distance = 10 pixels")
        # plt.subplot(2, 2, 4), plt.imshow(chopArray), \
        # plt.plot(peak_localmax_15[:, 1], peak_localmax_15[:, 0], 'r+'),plt.title("Minimum peaks distance = 15 pixels")
        # proposalCentersList.append(peak_localmax)
        # print len(proposalCentersList)
        # print len(peak_localmax)

    return proposalCentersList

def calPerformance(proposalCenterList, chopColNr, chopsize):
    """Validate the performance by calculating the recall"""
    rgb_ssearch_layer_name = "rgb_image_clipped"

    centerList = list()
    for i, chop_proposal in enumerate(proposalCenterList):
        shiftCol = i % chopColNr
        shiftRow = i / chopColNr
        shiftX, shiftY = (chopsize * shiftCol, chopsize * shiftRow)
        for centerX, centerY in chop_proposal:
            centerList.append((centerX + shiftX, centerY + shiftY))
    tools.createFeatureLayer(rgb_ssearch_layer_name, centerList, chopsize)
    tools.calCoverage()



# if __name__ == "__main__":
timeStart = time.time()
rgb_image_filename = "/Users/ping/Documents/thesis/data/proposal_test/rgb_image_clipped.tif"
chopsize = 1024
print "working on chopping..."
chopList, chopColNr, chopRowNr = cropImage(rgb_image_filename, chopsize)
print len(chopList), chopColNr, chopRowNr
print "working on detect proposals..."
proposalCenterList = detectProposals(chopList)
print "working on calculate performance..."
calPerformance(proposalCenterList, chopColNr, chopsize)

timeEnd = time.time()
timeUsed = timeEnd - timeStart
print "Time used for calculate performance is {0}".format(timeUsed/60)