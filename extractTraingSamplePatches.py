# from geo_utils import get_lat_long_from_top_left_point_in_tile
# from geo_utils import get_lat_long_from_bottom_right_point_in_tile
# from geo_utils import get_grid_area_size_from_bbox_lat_long
import os
from PyQt4.QtCore import *
from qgis.core import *
import gdal
import numpy as np


def getLayerByName(layer_name):
    layer = None
    for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
        if lyr.name() == layer_name:
            layer = lyr
            break
    return layer


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


def extractPatches(points_layer_name, raster_layer_name, patchSize):
    rgb_image_path = '/Users/ping/Documents/thesis/data/rgb_image.tif'
    image = gdal.Open(rgb_image_path).ReadAsArray()
    image = np.transpose(image, (1, 2, 0))
    image_height = float(image.shape[0])
    image_width = float(image.shape[1])
    patchesMatrixes = []

    extractedPatchesCentres = getPointPixelCoordinates(points_layer_name, raster_layer_name)

    for patch_center in extractedPatchesCentres:
        tl_x = int(patch_center.x() - patchSize / 2)
        tl_y = int(patch_center.y() - patchSize / 2)

        if tl_x + patchSize <= image_width and tl_y + patchSize <= image_height and tl_x >= 0 and tl_y >= 0:
            patchMatrix = image[tl_y:tl_y + patchSize, tl_x: tl_x + patchSize]
            patchesMatrixes.append(patchMatrix)

    return patchesMatrixes


def savePatchesAsNumpy(lowerOrUpper, trees, ptsLayer):
    patchesDir = '/Users/ping/Documents/thesis/data/patchesNumpyArrays'
    treePatchDir = patchesDir + '/' + str(lowerOrUpper) + '/' + trees + '/'

    # rgb_image_path = '/Users/nuistzhou/thesis/Kolovai-Trees-20180108/rgb_image.tif'
    # image = gdal.Open(rgb_image_path)

    patchesMatrix = extractPatches(ptsLayer, 'rgb_image', 90)
    for i, patchMatrix in enumerate(patchesMatrix):
        file_name = "{0:04}.npy".format(i)
        imageOutputPath = os.path.join(treePatchDir, file_name)
        # imsave(imageOutputPath, patchMatrix)
        np.save(imageOutputPath, patchMatrix)


# savePatchesAsPic('lower', 'coco', 'cocoTreesLowerLayer')
# savePatchesAsPic('lower', 'non_coco', 'non_cocoTreesLowerLayer')
# savePatchesAsPic('upper', 'coco', 'cocoTreesUpperLayer')
# savePatchesAsPic('upper', 'non_coco', 'non_cocoTreesUpperLayer')
