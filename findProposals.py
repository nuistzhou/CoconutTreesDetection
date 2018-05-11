import os
import numpy as np
import cv2
from PIL import Image
def cropImage(filename, chopsize):
    ## Load image
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
    normal_counter = 0
    small_counter = 0
    for j in range(chopRowNr):
        for i in range(chopColNr):
            tempArray = np.zeros((chopsize, chopsize, 3), dtype = np.int8)
            if i == chopColNr - 1 and j == chopRowNr -1:
                chopArray = image_raw[i * chopsize: (i * chopsize + pixelAddX),
                            j * chopsize: (j * chopsize + pixelAddY), :]
                tempArray[:pixelAddX, :pixelAddY, :] = chopArray
            elif i == chopColNr -1:
                chopArray = image_raw[i * chopsize: (i * chopsize + pixelAddX),
                            j * chopsize: (j + 1) * chopsize, :]
                tempArray[:pixelAddX, :, :] = chopArray
            elif j == chopRowNr -1:
                chopArray = image_raw[i * chopsize: (i + 1) * chopsize,
                            j * chopsize: (j * chopsize + pixelAddY), :]
                tempArray[:, :pixelAddY, :] = chopArray

            else:
                tempArray[:, :, :] = image_raw[i * chopsize: (i + 1) * chopsize,
                                     j * chopsize: (j + 1) * chopsize, :
                                     ]
            chopList.append(tempArray)
    print height, width
    return chopList, chopColNr, chopRowNr

def createImageFromCrops(chopsize, chopList, chopColNr, chopRowNr):
    array = np.zeros((chopsize * chopColNr, chopsize * chopRowNr, 3), dtype = np.int8)
    counter = 0
    for j in range(chopRowNr):
        for i in range(chopColNr):
            array[i * chopsize: (i + 1) * chopsize, j * chopsize : (j + 1) * chopsize, :] = chopList[counter]
            counter += 1
    array_new = np.transpose(array, (1,0,2))
    img = Image.fromarray(array_new, 'RGB')
    img.save('/Users/ping/Documents/thesis/data/rgb_image_ssearch/my.png')
    img.show()
    # print array_new.shape

def averageCocotrees():
    imageDir = "/Users/ping/Documents/thesis/data/patchImages/lower/coco"

    pass

def fourierTransform(cropList, cocotreeAvg):
    pass

if __name__ == "__main__":
    rgb_image_filename = "/Users/ping/Documents/thesis/data/rgb_image_ssearch/rgb_image_ssearch.tif"
    chopsize = 1024
    chopList, chopColNr, chopRowNr = cropImage(rgb_image_filename, chopsize)
    newImage = createImageFromCrops(chopsize, chopList, chopColNr, chopRowNr)
