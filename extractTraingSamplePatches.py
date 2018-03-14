#from geo_utils import get_lat_long_from_top_left_point_in_tile
#from geo_utils import get_lat_long_from_bottom_right_point_in_tile
#from geo_utils import get_grid_area_size_from_bbox_lat_long
from PyQt4.QtCore import *
from qgis.core import *


def getLayerByName(layer_name):
    layer=None
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
    
    
    
    
    
    
    
    