# from geo_utils import get_lat_long_from_top_left_point_in_tile
# from geo_utils import get_lat_long_from_bottom_right_point_in_tile
# from geo_utils import get_grid_area_size_from_bbox_lat_long
from config import Parameters
from qgis.gui import QgsRubberBand
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

# Desc: Find the stride size among 5,10,15,20 which gives the highest matching accuracy
# between sliding window and groundtruthing coconut trees patches

def getLayerByName(layer_name):
    # return the layer object
    registry = QgsMapLayerRegistry.instance()
    layer = registry.mapLayersByName(layer_name)[0]
    return layer


def createSlidingWindowLayer(strideSize):
    #### test
    # rubberbands = QgsRubberBand(iface.mapCanvas(), True)
    # rubberbands.setBorderColor(QColor(255, 0, 0))
    # rubberbands.setFillColor(QColor(0, 0, 0, 0))
    # rubberbands.setLineStyle(Qt.DotLine)
    # rubberbands.setWidth(3)
    #####

    slidingWindows = list() # A list of sliding window geometries
    rgbRasterLayer = getLayerByName("rgb_image")
    pixel_size_x = rgbRasterLayer.rasterUnitsPerPixelX()
    pixel_size_y = rgbRasterLayer.rasterUnitsPerPixelY()

    top_left_x = rgbRasterLayer.extent().xMinimum()
    top_left_y = rgbRasterLayer.extent().yMaximum()
    bottom_right_x = rgbRasterLayer.extent().xMaximum()
    bottom_right_y = rgbRasterLayer.extent().yMinimum()
    # bottom_right_x = -19518254
    # bottom_right_y = -2402279

    window_bottom_right_y = top_left_y - Parameters.samplePatchSize * pixel_size_y
    while window_bottom_right_y >= bottom_right_y:
        window_bottom_right_x = top_left_x + Parameters.samplePatchSize * pixel_size_x
        while window_bottom_right_x <= bottom_right_x:
            qgsPointsList = [QgsPoint(window_bottom_right_x - Parameters.samplePatchSize * pixel_size_x, window_bottom_right_y + Parameters.samplePatchSize * pixel_size_y),
                             QgsPoint(window_bottom_right_x, window_bottom_right_y + Parameters.samplePatchSize * pixel_size_x),
                             QgsPoint(window_bottom_right_x, window_bottom_right_y),
                             QgsPoint(window_bottom_right_x - Parameters.samplePatchSize * pixel_size_x, window_bottom_right_y)]
            windowGeometry = QgsGeometry.fromPolygon([qgsPointsList])
            slidingWindows.append(windowGeometry)
            # print windowGeometry
            # rubberbands.addGeometry(windowGeometry, None)
            window_bottom_right_x = window_bottom_right_x + strideSize
        window_bottom_right_y = window_bottom_right_y - strideSize
    # rubberbands.show()
    return slidingWindows

def createCocoPatches():
    rgbRasterLayer = getLayerByName("rgb_image")
    pixel_size_x = rgbRasterLayer.rasterUnitsPerPixelX()
    pixel_size_y = rgbRasterLayer.rasterUnitsPerPixelY()
    top_left_x = rgbRasterLayer.extent().xMinimum()
    top_left_y = rgbRasterLayer.extent().yMaximum()
    bottom_right_x = rgbRasterLayer.extent().xMaximum()
    bottom_right_y = rgbRasterLayer.extent().yMinimum()

    cocoTreesVecLayer = getLayerByName("coconutTrees")
    features = cocoTreesVecLayer.getFeatures()
    cocoPolygons = list()
    for cocoPatch in features:
        pt_x = cocoPatch.geometry().asPoint().x()
        pt_y = cocoPatch.geometry().asPoint().y()

        topLeft_x = pt_x - Parameters.samplePatchSize/2 * pixel_size_x
        topLeft_y = pt_y + Parameters.samplePatchSize/2 * pixel_size_y
        topRight_x = pt_x + Parameters.samplePatchSize/2 * pixel_size_x
        topRight_y = pt_y + Parameters.samplePatchSize/2 * pixel_size_y
        bottomLeft_x = pt_x - Parameters.samplePatchSize / 2 * pixel_size_x
        bottomLeft_y = pt_y - Parameters.samplePatchSize / 2 * pixel_size_y
        bottomRight_x = pt_x + Parameters.samplePatchSize/2 * pixel_size_x
        bottomRight_y = pt_y - Parameters.samplePatchSize/2 * pixel_size_y

        qgsPointsList = [QgsPoint(topLeft_x, topLeft_y),
                         QgsPoint(topRight_x, topRight_y),
                         QgsPoint(bottomRight_x,bottomRight_y),
                         QgsPoint(bottomLeft_x, bottomLeft_y)]
        windowGeometry = QgsGeometry.fromPolygon([qgsPointsList])
        cocoPolygons.append(windowGeometry)
    return cocoPolygons


def calculateAverageOverlappingPercentage(strideSize):
    """@type strideSize: int"""
    slidingWindowGeometryList = createSlidingWindowLayer(strideSize)
    cocoGeometryList = createCocoPatches()

    # print len(slidingWindowGeometryList)
    # print len(cocoGeometryList)
    area = QgsDistanceArea()
    area.setEllipsoid('WGS84')
    area.setEllipsoidalMode(True)

    cocoAveOverlappedPercentage = list()
    for cocoGeometry in cocoGeometryList:
        cocoPolygonArea = area.measurePolygon(cocoGeometry.asPolygon()[0])
        overlappedWindowList = list()
        for slidingWindowGeometry in slidingWindowGeometryList:
            if cocoGeometry.intersects(slidingWindowGeometry):
                intersection = slidingWindowGeometry.intersection(cocoGeometry)
                percentage_overlap = (area.measurePolygon(intersection.asPolygon()[0]) / cocoPolygonArea) * 100
                overlappedWindowList.append(percentage_overlap)
        if len(overlappedWindowList) != 0:
            cocoAveOverlappedPercentage.append(max(overlappedWindowList))
            # print "There are {0} overlappings".format(len(overlappedWindowList))

    # print sum(cocoAveOverlappedPercentage)/len(cocoAveOverlappedPercentage)
    # print len(cocoAveOverlappedPercentage)
    return sum(cocoAveOverlappedPercentage)/len(cocoAveOverlappedPercentage)



def getBestStrideSize():
    strideSizeOption = [5, 10, 15, 20]
    stridePermance = list()
    for strideSize in strideSizeOption:
        performance = calculateAverageOverlappingPercentage(strideSize)
        stridePermance.append(calculateAverageOverlappingPercentage(strideSize))
        print "Overlapping rate for stride size {0} is {1}".format(strideSize, performance)
    print stridePermance

# if __name__ == "__main__":
getBestStrideSize()