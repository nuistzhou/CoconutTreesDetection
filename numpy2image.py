import os
from PIL import Image
import numpy as np

inputDir = '/media/sf_Thesis/Data/Kolovai-Trees-20180108/patchesNumpyArrays/'
outputDir = '/media/sf_Thesis/Data/Kolovai-Trees-20180108/patchImages/'
list_filen_names = os.listdir(inputDir)
for file_name in list_filen_names:
    path_file_name = os.path.join(inputDir, file_name)
    np_array = np.load(path_file_name)
    image_file_name = os.path.join(outputDir, (file_name[:-4]+ '.png'))
    img = Image.fromarray(np_array, 'RGB')
    img.save(image_file_name)

