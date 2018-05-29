from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
import numpy as np
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.manifold import TSNE
import processing
from processing.core.Processing import Processing
Processing.initialize()
Processing.updateAlgsList()


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

def geoCoord2PixelPosition(point, top_left_x, top_left_y, pixel_size_x, pixel_size_y):
    pixPosX = int(round((point.x() - top_left_x) / pixel_size_x))
    pixPosY = int(round((top_left_y - point.y()) / pixel_size_y))
    return QgsPoint(pixPosX, pixPosY)


def getPointPixelCoordinates(points_layer_name, raster_layer_name):
    points_layer = getLayerByName(points_layer_name)
    features_iter = points_layer.getFeatures()
    features_array = []
    for feature in features_iter:
        features_array.append(feature)

    raster_layer = getLayerByName(raster_layer_name)
    pixel_size_x = raster_layer.rasterUnitsPerPixelX()
    pixel_size_y = raster_layer.rasterUnitsPerPixelY()
    top_left_x = raster_layer.extent().xMinimum()
    top_left_y = raster_layer.extent().yMaximum()
    pixel_coords_array = []
    for feature in features_array:
        point_crs_coord = feature.geometry().asPoint()
        point_pixel_coords = geoCoord2PixelPosition(point_crs_coord, top_left_x, top_left_y, pixel_size_x, pixel_size_y)
        pixel_coords_array.append(point_pixel_coords)
    return pixel_coords_array

def createFeatureLayer(rgbLayerName, pixCoordsList, chopsize):
    rgb_upper_layer = getLayerByName(rgbLayerName)
    rgb_crs = rgb_upper_layer.crs()

    pixel_size_x = rgb_upper_layer.rasterUnitsPerPixelX()
    pixel_size_y = rgb_upper_layer.rasterUnitsPerPixelY()
    top_left_x = rgb_upper_layer.extent().xMinimum()
    top_left_y = rgb_upper_layer.extent().yMaximum()

    # create layer
    vlayer = QgsVectorLayer("Point", "temporary_points", "memory")
    vlayer.setCrs(rgb_crs, False)
    # pr = vlayer.dataProvider()
    # Enter editing mode
    vlayer.startEditing()
    vlayer.addAttribute(QgsField("id", QVariant.Int))
    fields = vlayer.pendingFields()
    # add features
    for i, pixCoords in enumerate(pixCoordsList):
        fet = QgsFeature()
        fet.setFields(fields, True)
        x = top_left_x + pixCoords[0] * pixel_size_x
        y = top_left_y - pixCoords[1] * pixel_size_y
        fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(x, y)))
        fet["id"] = i
        vlayer.addFeatures([fet])
    vlayer.commitChanges()
    # Commit changes
    QgsMapLayerRegistry.instance().addMapLayer(vlayer)

def calCoverage():
    distNearestPointsFilename = "/Users/ping/Documents/thesis/data/proposal_test/nearest_point_distance.shp"
    tempPointsLayer = getLayerByName("temporary_points")
    cocoTreesLayer = getLayerByName("cocotrees_clipped")
    tempPointsLayer.removeSelection()
    cocoTreesLayer.removeSelection()
    processing.runalg('qgis:distancetonearesthub', cocoTreesLayer, tempPointsLayer,
                              'id',1, 4, distNearestPointsFilename)
    # Load layer from disk and display in the table of content
    distNearestPoints = QgsVectorLayer(distNearestPointsFilename, 'nearestPoints_distance', 'ogr')
    QgsMapLayerRegistry.instance().addMapLayer(distNearestPoints)
    # Count number of coconut trees in total
    # Select features which are within 15 pixels distance
    distance = 0.0859006 * 12 # 12 pixels distance in meters
    query = QgsExpression(r'"HubDist" <= {0}'.format(distance))
    selection = distNearestPoints.getFeatures(QgsFeatureRequest(query))
    ids = [k.id() for k in selection]
    distNearestPoints.setSelectedFeatures(ids)

    feats_count = cocoTreesLayer.featureCount()
    selectedFeats_count = distNearestPoints.selectedFeatureCount()
    coverage_percentage = float(selectedFeats_count) / float(feats_count) * 100
    print "The number of coconut trees in total is {0}".format(feats_count)
    print "Total number of proposals is {0}".format(tempPointsLayer.featureCount())
    print "The number of proposals within 15 pixels of coconut trees is {0}".format(selectedFeats_count)
    print "The proposals cover {:4.2f}% of all coconut annotations!".\
        format(coverage_percentage)
    QgsMapLayerRegistry.instance().removeMapLayers(["temporary_points", "nearestPoints_distance"])
    return coverage_percentage

def linearSVM_grid_search(dataset, labels):
    C_s = 10.0 ** np.arange(-1, 3)
    tuned_parameters = [{'C': C_s}]
    clf = GridSearchCV(svm.LinearSVC(C=1), tuned_parameters, cv=3)
    clf.fit(dataset, labels)
    return clf.best_params_['C']


def getTSNEFeatures(features):
    projection_area_height = 800
    projection_area_width = 420
    # get TSNE projection
    converter = TSNE(n_components=2, random_state=0)
    features2D = converter.fit_transform(features)
    # features2D = features2D * 6# scaling values
    print "TSNE ok"

    # compute scale factor
    print "orig x min {} max {}".format(np.min(features2D[:, 0]), np.max(features2D[:, 0]))
    print "orig y min {} max {}".format(np.min(features2D[:, 1]), np.max(features2D[:, 1]))
    x_min = np.min(features2D[:, 0])
    y_min = np.min(features2D[:, 1])
    x_max = np.max(features2D[:, 0])
    y_max = np.max(features2D[:, 1])
    scale_factor = projection_area_width / float(x_max - x_min)
    features2D = features2D * scale_factor
    print "scale factor {}".format(scale_factor)

    features2D[:, 0] = features2D[:, 0] - x_min
    features2D[:, 1] = features2D[:, 1] - y_min
    print "x min {} max {}".format(np.min(features2D[:, 0]), np.max(features2D[:, 0]))
    print "y min {} max {}".format(np.min(features2D[:, 1]), np.max(features2D[:, 1]))

    return features2D
