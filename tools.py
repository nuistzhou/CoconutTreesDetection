from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import QFileInfo

def getLayerByName(layer_name):
        layer = None
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() == layer_name:
                layer = lyr
                break
        return layer

def getRasterLayerByName(filename):
    """
    filename: String of layer file's path
    return the layer object"""
    fileInfo = QFileInfo(filename)
    path = fileInfo.filePath()
    baseName = "rgb"
    rlayer = QgsRasterLayer(path, baseName)
    return rlayer

def getVectorLayerByName(filename):
    layer = QgsVectorLayer(filename, "vector", "ogr")
    return layer

def pixel2XY(layer, pixel_x, pixel_y):
    rasterLayer = getRasterLayerByName(layer)
    # pixel_size_x = rasterLayer.rasterUnitsPerPixelX()
    pixel_size_x = 0.08590057817769892
    # pixel_size_y = rasterLayer.rasterUnitsPerPixelY()
    pixel_size_y = 0.08590057817774652

    # top_left_x = rasterLayer.extent().xMinimum()
    top_left_x = -19519759.96498842
    # top_left_y = rasterLayer.extent().yMaximum()
    top_left_y = -2402256.5553289615


    x = top_left_x + pixel_x * pixel_size_x
    y = top_left_y - pixel_y * pixel_size_y

    print x,y
    return (x, y)