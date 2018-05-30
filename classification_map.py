import numpy as np
from config import Parameters
from PIL import Image
from qgis.gui import *
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import gdal
import subprocess
import tools


def calPredictedProbsMatrix():
    test_labels = np.load('/Users/ping/Documents/thesis/data/result/test_labels.npy')
    predicted_probs = np.load("/Users/ping/Documents/thesis/data/result/predicted_probs.npy")
    dim_y = 1773
    dim_x = 5310
    classification_image = np.zeros((dim_y, dim_x), dtype = np.uint8)
    classification_map_sumup = np.zeros((dim_y, dim_x), dtype = np.uint8)
    predicted_probs_matrix = np.zeros((dim_y, dim_x), dtype = np.float)
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
                classification_image[window_top_left_y: window_bottom_right_y,
                              window_top_left_x: window_bottom_right_x] = 255
                classification_map_sumup[window_top_left_y: window_bottom_right_y,\
                              window_top_left_x: window_bottom_right_x] += 1
                predicted_probs_matrix[window_top_left_y: window_bottom_right_y,\
                              window_top_left_x: window_bottom_right_x] += predicted_probs[counter, 1]
                counterCoco += 1
            counter += 1
            window_top_left_x += Parameters.strideSize
            window_bottom_right_x += Parameters.strideSize
        window_top_left_y += Parameters.strideSize
        window_bottom_right_y += Parameters.strideSize
#
# print "Number of {0} coconut trees detected from {1} windows, with a percentage of " \
#       "{2: .2f}%!".format(counterCoco, counter, float(counterCoco)/counter * 100)

    predicted_probs_matrix_max = np.max(predicted_probs_matrix)
    predicted_probs_matrix = (predicted_probs_matrix/predicted_probs_matrix_max) * 255
    predicted_probs_matrix = predicted_probs_matrix.astype(np.uint8)
    img_summed_up_predicted_probs = Image.fromarray(predicted_probs_matrix)
    img_summed_up_predicted_probs.save("/Users/ping/thesis/data/result/classification_map_summed_up_probs.png")



def loadRasterLayer():
    # self.rstClassPathext = os.path.join(rstDirname, self.shpClassFileName + ".tif")
    #
    # gdal.AllRegister()
    # tifDrvr = gdal.GetDriverByName("GTiff")
    # # open input with GDAL
    # refRstrDt = gdal.Open(self.inputRaster, GA_ReadOnly)
    # # number of x pixels
    # refRstrCols = refRstrDt.RasterXSize
    # # number of y pixels
    # refRstrRows = refRstrDt.RasterYSize
    # # check projections
    # refRstrProj = refRstrDt.GetProjection()
    # # pixel size and origin
    # refRstGeoTrnsf = refRstrDt.GetGeoTransform()
    #
    # # Write Array into
    # inputRasterBand = refRstrDt.GetRasterBand(1)
    # dataTp = inputRasterBand.DataType
    # # ROIRaster = tifDrvr.Create(self.rstClassPathext, refRstrCols, refRstrRows, 1, dataTp)
    # ROIRaster = tifDrvr.Create(self.rstClassPathext, refRstrCols, refRstrRows, 1, gdal.GDT_UInt32)
    # ROIRaster.SetGeoTransform([refRstGeoTrnsf[0], refRstGeoTrnsf[1], 0, refRstGeoTrnsf[3], 0, refRstGeoTrnsf[5]])
    # ROIRaster.SetProjection(refRstrProj)
    # ROIRasterBand = ROIRaster.GetRasterBand(1)
    # ROIRasterBand.SetNoDataValue(0)
    # # write array
    # # class_labels = self.classification_labels.astype(np.uint32)
    # ROIRasterBand.WriteArray(self.classification_labels)
    # stat = ROIRasterBand.GetStatistics(0, 1)
    #
    # # close bands
    # ROIRasterBand = None
    # # close rasters
    # ROIRaster = None
    # refRstrDt = None
    inputImage = "/Users/ping/thesis/data/result/classification_map_summed_up_probs.png"
    outputImage = "/Users/ping/thesis/data/result/classification_map_summed_up_probs_georeferenced.tif"
    layer = QgsRasterLayer("/Users/ping/thesis/data/result/classification_map_summed_up_probs.png", "Probability_map")
    crs_layer = tools.getLayerByName("rgb_image_clipped")
    ext = crs_layer.extent()
    xmin = ext.xMinimum()
    xmax = ext.xMaximum()
    ymin = ext.yMinimum()
    ymax = ext.yMaximum()
    coords = "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax)
    crs = crs_layer.crs()
    layer.setCrs(crs)
    # Set transparent raster value
    rasterTransparency = layer.renderer().rasterTransparency()
    listPixels = []
    pixel = QgsRasterTransparency.TransparentThreeValuePixel()
    pixel.red = 255
    pixel.green = 255
    pixel.blue = 255
    pixel.percentTransparent = 100
    listPixels.append(pixel)
    rasterTransparency.setTransparentThreeValuePixelList(listPixels)
    layer.triggerRepaint()
    QgsMapLayerRegistry.instance().addMapLayer(layer)
    # subprocess.call('gdal_translate -ot FLOAT32 -of AAIGrid terrain.tif terrain.asc', shell=True)
    # gdal.Translate(outputImage, inputImage, )
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
    #colDic = {'black':'#000000', 'gray':'#333333','white':'#ffffff'}

    valueList =[min, interval, max]

    lst = [QgsColorRampShader.ColorRampItem(valueList[0], QColor(colDic['blue'])),
       QgsColorRampShader.ColorRampItem(valueList[1], QColor(colDic['yellow'])),
       QgsColorRampShader.ColorRampItem(valueList[2], QColor(colDic['red']))]

    #lst = [QgsColorRampShader.ColorRampItem(valueList[0], QColor(colDic['black'])),\
    #       QgsColorRampShader.ColorRampItem(valueList[1], QColor(colDic['gray'])), \
    #       QgsColorRampShader.ColorRampItem(valueList[2], QColor(colDic['white']))]

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
# print np.min(classification_map_sumup)
# print np.max(classification_map_sumup)
# img = Image.fromarray(classification_image)
# img_summed_up = Image.fromarray(classification_map_sumup)
# img.save("/Users/ping/thesis/data/result/classification_map.png")
# img_summed_up.save("/Users/ping/thesis/data/result/classification_map_summed_up.png")
