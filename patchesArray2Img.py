import os
from PIL import Image
import numpy as np

def numpy2Image(numpyDir, imgDir):
    inputRootDir = '/Users/ping/Documents/thesis/data/patchesNumpyArrays/'
    outputRootDir = '/Users/ping/Documents/thesis/data/patchImages/'

    inputDir = os.path.join(inputRootDir, numpyDir)
    outputDir = os.path.join(outputRootDir, imgDir)
    list_filen_names = os.listdir(inputDir)
    for file_name in list_filen_names:
        path_file_name = os.path.join(inputDir, file_name)
        np_array = np.load(path_file_name)
        image_file_name = outputDir + file_name[:-4] + '.png'
        img = Image.fromarray(np_array, 'RGB')
        img.save(image_file_name)



numpy2Image('lower/coco/', 'lower/coco/')
numpy2Image('lower/non_coco/', 'lower/non_coco/')
numpy2Image('upper/coco/', 'upper/coco/')
numpy2Image('upper/non_coco/', 'upper/non_coco/')




