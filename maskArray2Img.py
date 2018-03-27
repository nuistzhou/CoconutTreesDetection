import os
import numpy as np
from PIL import Image

maskUpperLayerDir= "/Users/nuistzhou/thesis/Kolovai-Trees-20180108/maskRgbImage/upper"
maskLowerLayerDir= "/Users/nuistzhou/thesis/Kolovai-Trees-20180108/maskRgbImage/lower"

maskTreesArrayFilename = "treesMaskMatrix.npy"
maskTreesImgFilename = "treesMaskImg.png"

maskUpperLayerArrayPath = os.path.join(maskUpperLayerDir, maskTreesArrayFilename)
maskLowerLayerArrayPath = os.path.join(maskLowerLayerDir, maskTreesArrayFilename)

maskUpperLayerImgFilePath = os.path.join(maskUpperLayerDir, maskTreesImgFilename)
maskLowerLayerImgFilePath = os.path.join(maskLowerLayerDir, maskTreesImgFilename)

maskUpperLayerArray = np.load(maskUpperLayerArrayPath)
maskLowerLayerArray = np.load(maskLowerLayerArrayPath)

maskUpperLayerArray = maskUpperLayerArray.astype(np.uint8)
maskLowerLayerArray = maskLowerLayerArray.astype(np.uint8)

maskUpperLayerImg = Image.fromarray(maskUpperLayerArray) # Mode set as 1 indicating black $ white
maskLowerLayerImg = Image.fromarray(maskLowerLayerArray)

maskUpperLayerImg.save(maskUpperLayerImgFilePath)
maskLowerLayerImg.save(maskLowerLayerImgFilePath)
