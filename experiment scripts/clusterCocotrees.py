import os
import time
import glob
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
from scipy.misc import imsave
from config import Parameters


def averageCocotrees(imgArrayList, index):
    # Load images into a list of Numpy Array
    w, h = imgArrayList[0].shape[:2]
    nrImages = len(imgArrayList)

    # Create a numpy array of floats to store the average (assume RGB images)
    avgImageArr = np.zeros((h, w, 3), np.float)
    # Build up average pixel intensities, casting each image as an array of floats
    for imgArray in imgArrayList:
        avgImageArr = avgImageArr + imgArray / nrImages
    avgImageArr = np.array(np.round(avgImageArr), dtype=np.uint8)
    np.save(os.path.join(Parameters.resultPath, 'avgCocotrees_{0}.npy'.format(index)), avgImageArr)
    # avgImg = Image.fromarray(avgImageArr, 'RGB')
    # avgImg.save(os.path.join(Parameters.resultPath, 'avgCocotrees_{0}.png'.format(index)))

def putImgAtCenter():
    targetSize = 1024
    imageDir = Parameters.resultPath
    os.chdir(imageDir)
    filenameList = glob.glob("avgCocotrees*.npy")
    for filename in filenameList:
        imgArray = np.float32(np.load(filename)) / 255.
        imgArray -= np.average(imgArray[:])

        w, h = imgArray.shape[:2]
        topLeftX = targetSize/2 - 90/2
        topLeftY = targetSize/2 - 90/2
        avgImageArr = np.zeros((targetSize, targetSize, 3), np.float32)

        if w < targetSize and h < targetSize:
            avgImageArr[topLeftX : topLeftX + w, topLeftY : topLeftY + h,:] = imgArray
            np.save(filename[:-4] + 'enlarged.npy', avgImageArr)
            # cv2.imwrite(filename, avgImageArr)
            # avgImg = Image.fromarray(avgImageArr, 'RGB')
            # imsave(filename, avgImageArr)
            # avgImg.save(filename)

def clusterCocotrees(nrClusters):
    """nrClusters: number of clusters."""
    timeStart = time.time()
    imgClusterDict = dict()
    for clusterIndex in range(nrClusters):
        imgClusterDict[clusterIndex] = list()

    imageDir = "/Users/ping/Documents/thesis/data/patchImages/lower/coco"
    os.chdir(imageDir)
    filenameList = glob.glob("*.png")
    imgArrayList = list()
    for im in filenameList:
        imgArray= np.array(Image.open(im), dtype=np.float)

        # Normalization for each image
        imgArrayNorm = np.empty(0, dtype=np.float)
        for i in range(3):
            imgArraySingleBandTemp = imgArray[:,:,i]
            imgArraySingleBandTemp = imgArraySingleBandTemp.flatten()
            imgArrayNorm = np.concatenate((imgArrayNorm, (imgArraySingleBandTemp - imgArraySingleBandTemp.mean()) / imgArraySingleBandTemp.std()))

        imgArrayList.append(imgArrayNorm)
    imgArrays = np.asarray(imgArrayList)
    k_means = KMeans(n_clusters= nrClusters, n_jobs=-1)
    imgArrays = imgArrays.reshape((imgArrays.shape[0], -1))
    k_means.fit(imgArrays)
    labelsList = k_means.labels_.tolist()
    for i in range(len(imgArrayList)):
        imgArray = np.array(Image.open(filenameList[i]), dtype=np.float)
        groupIndex = labelsList[i]
        imgClusterDict[groupIndex].append(imgArray)

    for key, imgArrayList in imgClusterDict.iteritems():
        averageCocotrees(imgArrayList, key)

    timeEnd = time.time()
    timeUsed = timeEnd - timeStart
    print "Time used for clustering the coconut trees imagery is {0}".format(timeUsed/60)

# clusterCocotrees(10)
# putImgAtCenter()