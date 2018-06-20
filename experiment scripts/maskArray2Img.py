import os
import numpy as np
from PIL import Image
from config import Parameters


# def maskArray2Img(maskUpperLayerDir, maskArrayFilename, ):


# maskUpperLayerDir= os.path.join(Parameters.dataPath, "maskRgbImage/upper")
# maskLowerLayerDir= os.path.join(Parameters.dataPath, "maskRgbImage/lower")
maskRandomUpperLayerDir= os.path.join(Parameters.dataPath, "maskRgbImage/upper")
maskRandomLowerLayerDir= os.path.join(Parameters.dataPath, "maskRgbImage/lower")



# maskTreesArrayFilename = "treesMaskMatrix.npy"
# maskTreesImgFilename = "treesMaskImg.png"
maskRandomArrayFilename = "randomMaskMatrix.npy"
maskRandomImgFilename = "randomMaskImg.png"



# maskUpperLayerArrayPath = os.path.join(maskUpperLayerDir, maskTreesArrayFilename)
# maskLowerLayerArrayPath = os.path.join(maskLowerLayerDir, maskTreesArrayFilename)
maskRandomUpperLayerArrayPath = os.path.join(maskRandomUpperLayerDir, maskRandomArrayFilename)
maskRandomLowerLayerArrayPath = os.path.join(maskRandomLowerLayerDir, maskRandomArrayFilename)


# maskRandomUpperLayerArrayPath = os.path.join(maskUpperLayerDir, maskTreesArrayFilename)
# maskRandomLowerLayerArrayPath = os.path.join(maskLowerLayerDir, maskTreesArrayFilename)

# maskUpperLayerImgFilePath = os.path.join(maskUpperLayerDir, maskTreesImgFilename)
# maskLowerLayerImgFilePath = os.path.join(maskLowerLayerDir, maskTreesImgFilename)
maskRandomUpperLayerImgFilePath = os.path.join(maskRandomUpperLayerDir, maskRandomImgFilename)
maskRandomLowerLayerImgFilePath = os.path.join(maskRandomLowerLayerDir, maskRandomImgFilename)
#
# maskUpperLayerArray = np.load(maskUpperLayerArrayPath)
# maskLowerLayerArray = np.load(maskLowerLayerArrayPath)
maskRandomUpperLayerArray = np.load(maskRandomUpperLayerArrayPath)
maskRandomLowerLayerArray = np.load(maskRandomLowerLayerArrayPath)

# maskUpperLayerArray = maskUpperLayerArray.astype(np.uint8)
# maskLowerLayerArray = maskLowerLayerArray.astype(np.uint8)
maskRandomUpperLayerArray = maskRandomUpperLayerArray.astype(np.uint8)
maskRandomLowerLayerArray = maskRandomLowerLayerArray.astype(np.uint8)

# maskUpperLayerImg = Image.fromarray(maskUpperLayerArray) # Mode set as 1 indicating black $ white
# maskLowerLayerImg = Image.fromarray(maskLowerLayerArray)
maskRandomUpperLayerImg = Image.fromarray(maskRandomUpperLayerArray) # Mode set as 1 indicating black $ white
maskRandomLowerLayerImg = Image.fromarray(maskRandomLowerLayerArray)


maskRandomUpperLayerImg.save(maskRandomUpperLayerImgFilePath)
maskRandomLowerLayerImg.save(maskRandomLowerLayerImgFilePath)
