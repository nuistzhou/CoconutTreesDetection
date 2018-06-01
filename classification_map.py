import numpy as np
from config import Parameters
from PIL import Image
from qgis.gui import *
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import gdal
from osgeo.gdalconst import *
import cv2
import tools

def calPredictedProbsMatrix(rgbImageFilename, test_labels, predicted_probs):
    # test_labels = np.load(Parameters.predictionLabels)
    # predicted_probs = np.load(Parameters.predictionProbs)

    imgArray = gdal.Open(rgbImageFilename).ReadAsArray().astype(np.uint8)
    imgArray = np.transpose(imgArray, (1, 2, 0))
    dim_y, dim_x  = imgArray.shape[:-1]
    # classification_image = np.zeros((dim_y, dim_x), dtype = np.uint8)
    # classification_map_sumup = np.zeros((dim_y, dim_x), dtype = np.uint8)
    predicted_probs_matrix = np.zeros((dim_y, dim_x), dtype = np.float32)
    window_top_left_y = 0
    window_bottom_right_y = 90
    counter = 0
    counterCoco = 0
    print Parameters.strideSize

    while window_bottom_right_y < dim_y - Parameters.samplePatchSize:
        window_bottom_right_x = 90
        window_top_left_x = 0
        while (window_bottom_right_x < dim_x - Parameters.samplePatchSize):
            if test_labels[counter] == 1:
                predicted_probs_matrix[window_top_left_y: window_bottom_right_y,\
                              window_top_left_x: window_bottom_right_x] += predicted_probs[counter, 1]
                counterCoco += 1
            counter += 1
            window_top_left_x += Parameters.strideSize
            window_bottom_right_x += Parameters.strideSize
        window_top_left_y += Parameters.strideSize
        window_bottom_right_y += Parameters.strideSize

    return predicted_probs_matrix


def loadRasterLayer(predicted_probs_matrix, inputImage, rstClassPathext, probsLayerName):
    """Georeference the classification probability map and load into QGIS"""

    # rstClassPathext = Parameters.rstClassPathext
    # inputImage = "/Users/ping/thesis/data/result/rgb_image_clipped_png.png"
    # inputImage = Parameters.rgb_image
    gdal.AllRegister()
    tifDrvr = gdal.GetDriverByName("GTiff")
    # open input with GDAL
    refRstrDt = gdal.Open(inputImage, GA_ReadOnly)
    # number of x pixels
    refRstrCols = refRstrDt.RasterXSize
    # number of y pixels
    refRstrRows = refRstrDt.RasterYSize
    # check projections
    refRstrProj = refRstrDt.GetProjection()
    # pixel size and origin
    refRstGeoTrnsf = refRstrDt.GetGeoTransform()

    # Write Array into
    inputRasterBand = refRstrDt.GetRasterBand(1)
    dataTp = inputRasterBand.DataType
    predicted_probs_matrix = predicted_probs_matrix.astype(np.uint32)
    ROIRaster = tifDrvr.Create(rstClassPathext, refRstrCols, refRstrRows, 1, gdal.GDT_UInt32)
    ROIRaster.SetGeoTransform([refRstGeoTrnsf[0], refRstGeoTrnsf[1], 0, refRstGeoTrnsf[3], 0, refRstGeoTrnsf[5]])
    ROIRaster.SetProjection(refRstrProj)
    ROIRasterBand = ROIRaster.GetRasterBand(1)
    ROIRasterBand.SetNoDataValue(0)
    # write array
    ROIRasterBand.WriteArray(predicted_probs_matrix)
    # close bands
    ROIRasterBand = None
    # close rasters
    ROIRaster = None
    refRstrDt = None
    layer = QgsRasterLayer(rstClassPathext, probsLayerName)
    QgsMapLayerRegistry.instance().addMapLayer(layer)
    return layer

def styleProbabilityMapRasterLayer(layer):
    renderer = layer.renderer()
    provider = layer.dataProvider()

    ver = provider.hasStatistics(1, QgsRasterBandStats.All)

    #stats = provider.bandStatistics(1, QgsRasterBandStats.All,extent, 0)
    stats = provider.bandStatistics(1, QgsRasterBandStats.All)

    if ver is not False:
        print "minimumValue = ".format(stats.minimumValue)
        print "maximumValue = ".format(stats.maximumValue)

    if (stats.minimumValue < 0):
        min = 0
    else:
        min= stats.minimumValue

    max = stats.maximumValue
    range = max - min
    add = range//2
    interval = min + add
    colDic = {'red':'#ff0000', 'yellow':'#ffff00','blue':'#0000ff'}

    valueList =[min, interval, max]

    lst = [QgsColorRampShader.ColorRampItem(valueList[0], QColor(colDic['blue'])),
       QgsColorRampShader.ColorRampItem(valueList[1], QColor(colDic['yellow'])),
       QgsColorRampShader.ColorRampItem(valueList[2], QColor(colDic['red']))]
    myRasterShader = QgsRasterShader()
    myColorRamp = QgsColorRampShader()

    myColorRamp.setColorRampItemList(lst)
    myColorRamp.setColorRampType(QgsColorRampShader.INTERPOLATED)
    myRasterShader.setRasterShaderFunction(myColorRamp)

    myPseudoRenderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(),
                                                    layer.type(),
                                                    myRasterShader)
    myPseudoRenderer.setOpacity(0.5)
    layer.setRenderer(myPseudoRenderer)
    layer.triggerRepaint()
