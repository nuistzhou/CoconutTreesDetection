import os
import numpy as np
import gdal
from random import randint
import pickle
from PIL import Image
from config import Parameters



def extractRandomPatchCenterFromList(maskMatrix, numberOfSamples):
    maskWidth = maskMatrix.shape[1]
    maskHeight = maskMatrix.shape[0]
    available_row, available_col = np.where(maskMatrix == 0)
    sizeOfAvailableSamples = len(available_row)
    counter = 0
    patchCenterArrayList = list()
    while sizeOfAvailableSamples > 0 and counter < numberOfSamples:
        index = randint(0, sizeOfAvailableSamples - 1)
        center_y, center_x = (available_row[index], available_col[index])

        if ((center_y - Parameters.samplePatchSize <0) or (center_x - Parameters.samplePatchSize < 0)
            or (center_y + Parameters.samplePatchSize > maskHeight) or
            (center_x + Parameters.samplePatchSize > maskWidth)):
            continue
        tl_x = int(center_x - Parameters.maskPatchSize / 2)
        tl_y = int(center_y - Parameters.maskPatchSize / 2)

        br_x = tl_x + Parameters.maskPatchSize
        br_y = tl_y + Parameters.maskPatchSize

        # Replace with boundary when beyond
        tl_x = max(tl_x, 0)
        tl_y = max(tl_y, 0)
        br_x = min(br_x, maskWidth - 1)
        br_y = min(br_y, maskHeight - 1)


        patchCenterArrayList.append((center_x, center_y))

        maskMatrix[tl_y: br_y + 1, tl_x: br_x + 1] = 255

        available_row, available_col = np.where(maskMatrix == 0)
        sizeOfAvailableSamples = len(available_row)
        counter += 1
        print counter

    return patchCenterArrayList, maskMatrix

def extractRandomPatchCenterFromListWithoutMask(numberOfSamples, imgHeight, imgWidth):
    counter = 0
    patchCenterArrayList = list()
    while counter < numberOfSamples:
        center_y = randint(0, imgHeight - 1)
        center_x = randint(0, imgWidth - 1)

        if ((center_y - Parameters.samplePatchSize <0) or (center_x - Parameters.samplePatchSize < 0)
            or (center_y + Parameters.samplePatchSize > imgHeight) or
            (center_x + Parameters.samplePatchSize > imgWidth)):
            continue
        patchCenterArrayList.append((center_x, center_y))
        counter += 1

    return patchCenterArrayList

def extractRandomPatchesAsNpy(randomPatchesCenterArrayList, upperOrLower):
    image = gdal.Open(Parameters.rgbImage).ReadAsArray()
    image = np.transpose(image, (1, 2, 0))
    image_upper = gdal.Open(os.path.join(Parameters.rgbImageUpper)).ReadAsArray()
    image_upper = np.transpose(image_upper, (1, 2, 0))
    image_upper_height = int(image_upper.shape[0])

    for i, randomPatchCenterTuple in enumerate(randomPatchesCenterArrayList):
        i = i +2000
        file_name = upperOrLower + '/random/' + "{0:04}.npy".format(i)
        patchArrayName = os.path.join(Parameters.patchesNumpyArray, file_name)
        center_x, center_y = randomPatchCenterTuple
        if upperOrLower == 'lower':
            center_y = center_y + image_upper_height
        tl_y = center_y - Parameters.samplePatchSize
        tl_x = center_x - Parameters.samplePatchSize

        patchMatrix = image[tl_y:tl_y + Parameters.samplePatchSize, tl_x: tl_x + Parameters.samplePatchSize]
        np.save(patchArrayName, patchMatrix)

def patchesNpy2Image(patchesNpyPath, outputDir):
    patchesNpyFilenameList = os.listdir(patchesNpyPath)
    for patchesNpyFilename in patchesNpyFilenameList:
        patchNpyFile = np.load(os.path.join(patchesNpyPath, patchesNpyFilename))
        image_file_name = outputDir + '/' + patchesNpyFilename[:-4] + '.png'
        img = Image.fromarray(patchNpyFile, 'RGB')
        img.save(image_file_name)

def main():

    treesUpperLayerMaskMatrix = np.load(os.path.join(Parameters.maskRgbImage, "upper/randomMaskMatrix_2000.npy"))
    randomUpperPatchesNpyList, maskMatrixUpper  = extractRandomPatchCenterFromList(treesUpperLayerMaskMatrix, 500)
    np.save("/Users/ping/Documents/thesis/data/maskRgbImage/upper/randomMaskMatrix_2500.npy", maskMatrixUpper)
    with open(os.path.join(Parameters.maskRgbImage, 'upper/randomUpperPatchesNpyList_500.pkl'), 'w+') as f:
        pickle.dump(randomUpperPatchesNpyList, f)

    treesLowerLayerMaskMatrix = np.load(os.path.join(Parameters.maskRgbImage, "lower/randomMaskMatrix_2000.npy"))
    randomLowerPatchesNpyList, maskMatrixLower  = extractRandomPatchCenterFromList(treesLowerLayerMaskMatrix, 500)
    np.save("/Users/ping/Documents/thesis/data/maskRgbImage/lower/randomMaskMatrix_2500.npy", maskMatrixLower)
    with open(os.path.join(Parameters.maskRgbImage, 'lower/randomLowerPatchesNpyList_500.pkl'), 'w+') as f:
        pickle.dump(randomLowerPatchesNpyList, f)


    extractRandomPatchesAsNpy(randomLowerPatchesNpyList, 'lower')
    extractRandomPatchesAsNpy(randomUpperPatchesNpyList, 'upper')

    patchesNpy2Image('/Users/ping/Documents/thesis/data/patchesNumpyArrays/lower/random', '/Users/ping/thesis/data/patchImages/lower/random')
    patchesNpy2Image('/Users/ping/Documents/thesis/data/patchesNumpyArrays/upper/random', '/Users/ping/thesis/data/patchImages/upper/random')

if __name__ == '__main__':
    main()