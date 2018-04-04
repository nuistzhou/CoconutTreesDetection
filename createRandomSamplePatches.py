import os
import numpy as np
from random import randint
from config import Parameters


def extractRandomPatchCenter(maskMatrix, number_needed):
    """Return new mask and random samples centre's list"""
    found = 0
    max_x = maskMatrix.shape[1]
    max_y = maskMatrix.shape[0]
    x = randint(0, max_x - 1)
    y = randint(0, max_y - 1)
    randomMasksList = list()

    while found < number_needed:
            if maskMatrix[y, x] == 0: # Zero means unmasked yet
                randomMasksList.append((x,y))
                # Create the mask
                tl_x = int(x - Parameters.maskPatchSize / 2)
                tl_y = int(y - Parameters.maskPatchSize / 2)

                br_x = tl_x + Parameters.maskPatchSize
                br_y = tl_y + Parameters.maskPatchSize

                # Replace with boundary when beyond
                tl_x = max(tl_x, 0)
                tl_y = max(tl_y, 0)
                br_x = min(br_x, max_x - 1)
                br_y = min(br_y, max_y - 1)

                maskMatrix[tl_y: br_y + 1, tl_x: br_x + 1] = 255  # Fill the box with value 255 as a mask
                found += 1 # Found +1

    return maskMatrix, randomMasksList

def main():
    f = open(os.path.join(Parameters.dataPath, 'maskRgbImage/randomPatchesCentres'), 'w+')
    treesUpperLayerMaskMatrix = np.load(os.path.join(Parameters.maskRgbImage, "upper/treesMaskMatrix.npy"))
    treesLowerLayerMaskMatrix = np.load(os.path.join(Parameters.maskRgbImage, "lower/treesMaskMatrix.npy"))


    maskMatrixUpper, randomUpperPatchesCenterList = extractRandomPatchCenter(treesUpperLayerMaskMatrix, 200)
    maskMatrixLower, randomLowerPatchesCenterList = extractRandomPatchCenter(treesLowerLayerMaskMatrix, 200)

    np.save("/Users/ping/thesis/data/maskRgbImage/upper/randomMaskMatrix.npy", maskMatrixUpper)
    np.save("/Users/ping/thesis/data/maskRgbImage/lower/randomMaskMatrix.npy", maskMatrixLower)
    for center in randomUpperPatchesCenterList:
        f.write("%s' '" % center)
    f.write('Follwoing is the lower layer: \n')
    for center in randomLowerPatchesCenterList:
        f.write("%s' '" % center)


if __name__ == '__main__':
    main()