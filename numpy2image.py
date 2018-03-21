import os
from PIL import Image
import numpy as np

inputDir = '/Users/nuistzhou/thesis/Kolovai-Trees-20180108/patchesNumpyArrays/'
outputDir = '/Users/nuistzhou/thesis/Kolovai-Trees-20180108/patchImages/'
list_filen_names = os.listdir(inputDir)
for file_name in list_filen_names:
    path_file_name = os.path.join(inputDir, file_name)
    np_array = np.load(path_file_name)
    image_file_name = os.path.join(outputDir, (file_name[:-4]+ '.png'))
    img = Image.fromarray(np_array, 'RGB')
    img.save(image_file_name)

