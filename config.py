import os

class Parameters:
    # Define some dataset path to be easily used later
    dataPath = "/Users/ping/thesis/data"
    samplePatchSize = 90
    maskPatchSize = 90*2
    rgbImage = os.path.join(dataPath, "rgb_image.tif")
    patchesNumpyArray = os.path.join(dataPath, "patchesNumpyArrays")
    rgbImageUpper = os.path.join(dataPath, 'rgb_image_upperLayer.tif')
    featureDescriptorPath = os.path.join(dataPath, "featureDescriptors")
    mergedFeatureDescriptorPath = os.path.join(dataPath, "featureDescriptors/merged_features")
    bowFeatureDescriptorPath = os.path.join(dataPath, "featureDescriptors/bow_features")
    performanceTestDir = os.path.join(dataPath, "performance_test")
    annotationFile = os.path.join(dataPath, "annotation.pkl")
    maskRgbImage = os.path.join(dataPath, "maskRgbImage")

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

