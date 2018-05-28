import os

class Parameters:
    # Define some dataset path to be easily used later
    dataPath = "/Users/ping/Documents/thesis/data"
    samplePatchSize = 90
    maskPatchSize = 90*2
    strideSize = 25
    bovwCodebookNrRandomSamples = 1000
    cocoVecLayer = "coconutTrees"
    rgbImage = os.path.join(dataPath, "rgb_image.tif")
    patchesNumpyArray = os.path.join(dataPath, "patchesNumpyArrays")
    rgbImageUpper = os.path.join(dataPath, 'rgb_image_upperLayer.tif')
    featureDescriptorPath = os.path.join(dataPath, "featureDescriptors")
    mergedFeatureDescriptorPath = os.path.join(dataPath, "featureDescriptors/merged_features")
    bowFeatureDescriptorPath = os.path.join(dataPath, "featureDescriptors/bow_features")
    performanceTestDir = os.path.join(dataPath, "performance_test")
    annotationCocoFile = os.path.join(dataPath, "annotationCoco.pkl")
    annotationNoncocoFile = os.path.join(dataPath, "annotationNoncoco.pkl")

    maskRgbImage = os.path.join(dataPath, "maskRgbImage")
    avgCocoImg = os.path.join(dataPath, "result/avgCoco.png")
    avgCocoImgEnlarged = os.path.join(dataPath, "result/avgCocoEnlarged.png")
    resultPath = "/Users/ping/Documents/thesis/results"

    def __init__(self, layer):
        self.layer = layer
        self.pixSizeX = None #Pixel size of X axis
        self.pixSizeY = None #Pixel size of Y axis
        self.topLeftX = None #Geo coordinate X of the Top Left pixel
        self.topLeftY = None #Geo coordinate Y of the Top Left pixel
        self.boundingboxSize = 40 # unit: pixel

    def readRasterConfig(self):
        self.pixSizeX = self.layer.rasterUnitsPerPixelX()
        self.pixSizeY = self.layer.rasterUnitsPerPixelY()
        self.topLeftX = self.layer.extent().xMinimum()
        self.topLeftY = self.layer.extent().yMaximum()

