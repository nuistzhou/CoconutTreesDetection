import os

class Parameters:
    # Define some dataset path to be easily used later
    dataPath = "/Users/ping/Documents/thesis/data"
    samplePatchSize = 90
    maskPatchSize = 90*2
    strideSize = 15
    bovwCodebookNrRandomSamples = 500
    cocoVecLayer = "coconutTrees"
    tempDir = os.path.join(dataPath, "temp")
    rgbImage = os.path.join(dataPath, "rgb_image.tif")
    rgb_image_clipped_png = "/Users/ping/Documents/thesis/data/result/rgb_image_clipped.png"
    patchesNumpyArray = os.path.join(dataPath, "patchesNumpyArrays")
    rgbImageUpper = os.path.join(dataPath, 'rgb_image_upperLayer.tif')
    featureDescriptorPath = os.path.join(dataPath, "featureDescriptors")
    mergedFeatureDescriptorPath = os.path.join(dataPath, "featureDescriptors/merged_features")
    bowFeatureDescriptorPath = os.path.join(dataPath, "featureDescriptors/bow_features")
    performanceTestDir = os.path.join(dataPath, "performance_test")

    maskRgbImage = os.path.join(dataPath, "maskRgbImage")
    avgCocoImg = os.path.join(dataPath, "result/avgCoco.png")
    avgCocoImgEnlarged = os.path.join(dataPath, "result/avgCocoEnlarged.png")
    resultPath = "/Users/ping/Documents/thesis/results"

    # To be moved after each phase
    predictionLabels = os.path.join(tempDir, "split1/test_labels.npy")
    predictionProbs = os.path.join(tempDir, "split1/predicted_probs.npy")
    rstClassPathext = os.path.join(tempDir, "split1/resultClassification_map_summed_up_probs.tif")
    trainedModelPath = os.path.join(tempDir, 'split1/trainedModel.pkl')
    annotationCocoFile = os.path.join(tempDir, "split1/annotationCoco.pkl")
    annotationNoncocoFile = os.path.join(dataPath, "split1/annotationNoncoco.pkl")

    # No move
    rgb_image_layername = "rgb_image_split1"
    groundTruthLayername = "coconut_split1"
    rgb_image_clipped_tif = os.path.join(tempDir, "split1/rgb_image_split1.tif")
    testFeatures = os.path.join(tempDir, "split1/testFeatures.npy")
    # and ground truths shapefile

    #For all different images
    codebookFileName = os.path.join(tempDir, "codebook.npy")

    # Validation
    validationImage = os.path.join(tempDir, "split2/rgb_image_split2.tif")
    rstClassPathextValidation = os.path.join(tempDir, "split2/validationClassification_map_summed_up_probs_split2.tif")
    rgb_image_layername_validation = "rgb_image_split2"
    groundTruthLayername_validation = "coconut_split2"
    predictionLabels_validation = os.path.join(tempDir, "split2/test_labels.npy")
    predictionProbs_validation = os.path.join(tempDir, "split2/predicted_probs.npy")
    validationFeatures = os.path.join(tempDir, 'split2/validationFeatures.npy')


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

