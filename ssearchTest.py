from selectiveSearch import ssearch
from config import Parameters
# from qgis.gui import QgsRubberBand
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from tools import getRasterLayerByName
from tools import getVectorLayerByName
from tools import getLayerByName
from tools import pixel2XY

def createCocoPatches():
    # rgbRasterLayer = getRasterLayerByName("/Users/ping/Documents/thesis/data/rgb_image_ssearch/rgb_image_ssearch.tif")
    # pixel_size_x = rgbRasterLayer.rasterUnitsPerPixelX()
    # pixel_size_y = rgbRasterLayer.rasterUnitsPerPixelY()
    pixel_size_x = 0.08590057817769892
    pixel_size_y = 0.08590057817774652

    cocoTreesVecLayer = getLayerByName("coconutTrees_ssearch")
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
        print windowGeometry
    return cocoPolygons

def createSsearchProposals():
    sselectiveWindows = list()  # A list of sliding window geometries
    rgb_image_ssearch = "/Users/ping/Documents/thesis/data/rgb_image_ssearch/rgb_image_ssearch.tif"
    ssearchProposals = ssearch(rgb_image_ssearch, 'f')
    for x, y, w, h in ssearchProposals:
        topLeft = pixel2XY(rgb_image_ssearch, x, y)
        topRight = pixel2XY(rgb_image_ssearch, x + w, y)
        bottomRight = pixel2XY(rgb_image_ssearch, x + w, y + h)
        bottomLeft = pixel2XY(rgb_image_ssearch, x, y + h)

        qgsPointsList = [QgsPoint(topLeft[0], topLeft[1]),
                         QgsPoint(topRight[0], topRight[1]),
                         QgsPoint(bottomRight[0], bottomRight[1]),
                         QgsPoint(bottomLeft[0], bottomLeft[1])]

        windowGeometry = QgsGeometry.fromPolygon([qgsPointsList])
        sselectiveWindows.append(windowGeometry)
    print "Number of {0} proposal windows created!".format(len(sselectiveWindows))
    return sselectiveWindows

def avgBestOverlap():
    """@type strideSize: int"""
    ssearchProposals = createSsearchProposals()
    cocoGeometryList = createCocoPatches()
    print "Number of {0} cocotrees geometry was created".format(len(cocoGeometryList))

    # print len(slidingWindowGeometryList)
    # print len(cocoGeometryList)
    area = QgsDistanceArea()
    area.setEllipsoid('WGS84')
    area.setEllipsoidalMode(True)

    cocoAveOverlappedPercentage = list()
    for cocoGeometry in cocoGeometryList:
        cocoPolygonArea = area.measurePolygon(cocoGeometry.asPolygon()[0])
        overlappedWindowList = list()
        for proposalWindow in ssearchProposals:
            if cocoGeometry.intersects(proposalWindow):
                polygonUnion = cocoGeometry.combine(proposalWindow)
                UnionedPolygonArea = area.measurePolygon(polygonUnion.asPolygon()[0])
                intersection = proposalWindow.intersection(cocoGeometry)
                intersectionArea = area.measurePolygon(intersection.asPolygon()[0])
                percentage_overlap = (intersectionArea / UnionedPolygonArea) * 100
                overlappedWindowList.append(percentage_overlap)
        if len(overlappedWindowList) != 0:
            cocoAveOverlappedPercentage.append(max(overlappedWindowList))

    return sum(cocoAveOverlappedPercentage)/len(cocoGeometryList)

print avgBestOverlap()