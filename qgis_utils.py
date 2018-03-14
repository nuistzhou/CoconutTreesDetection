#from geo_utils import get_lat_long_from_top_left_point_in_tile
#from geo_utils import get_lat_long_from_bottom_right_point_in_tile
#from geo_utils import get_grid_area_size_from_bbox_lat_long
from PyQt4.QtCore import *

def getLayerByName(layer_name):
    layer=None
    for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
        if lyr.name() == layer_name:
            layer = lyr
            break
    return layer

def addTopLeftMiniSquare(rect_layer, clip_layer):
	# get rectangular polygon
	rect_feature = rect_layer.getFeatures().next()
	rect_pol = rect_feature.geometry().asPolygon()
	nelems = len(rect_pol[0])
	#for i in range(nelems):
	#  print rect_pol[0][i]

	# create new polygon
	top_left = rect_pol[0][0]
	sp_eps = 0.0000001
	#top_left.x()
	pt1_tl = QgsPoint(top_left.x()-sp_eps, top_left.y()-(-sp_eps))
	pt2_tl = QgsPoint(top_left.x()-sp_eps, top_left.y())
	pt3_tl = QgsPoint(top_left.x(), top_left.y())
	pt4_tl = QgsPoint(top_left.x(), top_left.y() - (-sp_eps))
	tlmini_points = [pt1_tl, pt2_tl, pt3_tl, pt4_tl]
	tlmini_pol = [QgsPoint(i[0],i[1]) for i in tlmini_points]
	tlmini_geo = QgsGeometry.fromPolygon([tlmini_pol])

	# add new feature
	provider = clip_layer.dataProvider()
	f = QgsFeature()
	f.setGeometry(tlmini_geo)
	fields = clip_layer.pendingFields()
	f.initAttributes(fields.count())
	for i in range(fields.count()):
	  f.setAttribute(i,provider.defaultValue(i))
	#clip_layer.beginEditCommand("Feature added")
	clip_layer.startEditing()
	clip_layer.addFeature(f)
	clip_layer.commitChanges()
	#clip_layer.endEditCommand()

def addBottomRightMiniSquare(rect_layer, clip_layer):
	# get rectangular polygon
	rect_feature = rect_layer.getFeatures().next()
	rect_pol = rect_feature.geometry().asPolygon()
	nelems = len(rect_pol[0])
	#for i in range(nelems):
	#  print rect_pol[0][i]

	# create new polygon 
	bottom_right = rect_pol[0][2]
	sp_eps = 0.0000001
	#bottom_right.x()
	pt1_tl = QgsPoint(bottom_right.x(), bottom_right.y())
	pt2_tl = QgsPoint(bottom_right.x()+sp_eps, bottom_right.y())
	pt3_tl = QgsPoint(bottom_right.x()+sp_eps, bottom_right.y()+(-sp_eps))
	pt4_tl = QgsPoint(bottom_right.x(), bottom_right.y() + (-sp_eps))
	tlmini_points = [pt1_tl, pt2_tl, pt3_tl, pt4_tl]
	tlmini_pol = [QgsPoint(i[0],i[1]) for i in tlmini_points]
	tlmini_geo = QgsGeometry.fromPolygon([tlmini_pol])

	# add new feature
	provider = clip_layer.dataProvider()
	f = QgsFeature()
	f.setGeometry(tlmini_geo)
	fields = clip_layer.pendingFields()
	f.initAttributes(fields.count())
	for i in range(fields.count()):
	  f.setAttribute(i,provider.defaultValue(i))
	#clip_layer.beginEditCommand("Feature added")
	clip_layer.startEditing()
	clip_layer.addFeature(f)
	clip_layer.commitChanges()
	#clip_layer.endEditCommand()

def createValidRectangle(rect_layer, valid_rect_layer, zoom):
	# get rectangular polygon
	rect_feature = rect_layer.getFeatures().next()
	rect_pol = rect_feature.geometry().asPolygon()
	nelems = len(rect_pol[0])

	# get top left coordinate
	top_left_rect = rect_pol[0][0]
	bottom_right_rect = rect_pol[0][2]

	top_left = get_lat_long_from_top_left_point_in_tile(top_left_rect.y(), top_left_rect.x(), zoom)
	bottom_right = get_lat_long_from_bottom_right_point_in_tile(bottom_right_rect.y(), bottom_right_rect.x(), zoom)

	top_left = QgsPoint(top_left.x, top_left.y)
	bottom_right = QgsPoint(bottom_right.x, bottom_right.y)

	# compute new polygon
	pt1 = QgsPoint(top_left.x(), top_left.y())
	pt2 = QgsPoint(bottom_right.x(), top_left.y())
	pt3 = QgsPoint(bottom_right.x(), bottom_right.y())
	pt4 = QgsPoint(top_left.x(), bottom_right.y())

	valrect_points = [pt1, pt2, pt3, pt4]
	valrect_pol = [QgsPoint(i[0],i[1]) for i in valrect_points]
	valrect_geo = QgsGeometry.fromPolygon([valrect_pol])

	raster_shape_wh = get_grid_area_size_from_bbox_lat_long(top_left.y(), top_left.x(), bottom_right.y(), bottom_right.x(), zoom)

	# add new feature
	provider = valid_rect_layer.dataProvider()
	f = QgsFeature()
	f.setGeometry(valrect_geo)
	fields = valid_rect_layer.pendingFields()
	f.initAttributes(fields.count())
	for i in range(fields.count()):
	  f.setAttribute(i,provider.defaultValue(i))
	#valid_rect_layer.beginEditCommand("Feature added")
	valid_rect_layer.startEditing()
	valid_rect_layer.addFeature(f)
	valid_rect_layer.commitChanges()
	#valid_rect_layer.endEditCommand()
	return raster_shape_wh

def showRectangleCoordinates(rect_layer):
	# get rectangular polygon
	rect_feature = rect_layer.getFeatures().next()
	rect_pol = rect_feature.geometry().asPolygon()
	nelems = len(rect_pol[0])
	top_left_rect = rect_pol[0][0]
	bottom_right_rect = rect_pol[0][2]
	print "top_left_rect (lat, long) : ({}, {})".format(top_left_rect.y(), top_left_rect.x())
	print "bottom_right_rect (lat, long) : ({}, {})".format(bottom_right_rect.y(), bottom_right_rect.x())
	return ( (top_left_rect.y(), top_left_rect.x()), (bottom_right_rect.y(), bottom_right_rect.x()) )

def setLayerAttributeValues(layer, index_attribute, value):
	features = layer.getFeatures()
	layer.startEditing()
	for feat in features:
		layer.changeAttributeValue(feat.id(), index_attribute, value)
	layer.commitChanges()

def createNewVectorLayer(name):
    vl = QgsVectorLayer("Polygon", name, "memory")
    pr = vl.dataProvider()
    vl.startEditing()
    pr.addAttributes( [ QgsField("id", QVariant.Int) ] )
    vl.commitChanges()
    QgsMapLayerRegistry.instance().addMapLayer(vl)
    return vl

def writeVectorLayer(vector_layer, filename, output_dir):
	output_path = output_dir + filename + ".shp"
	vector_writer = QgsVectorFileWriter.writeAsVectorFormat(vector_layer, output_path, "utf-8", None, "ESRI Shapefile", False)

def writeClipLayer(layer, selector_layer_name, output_filename, output_dir):
	output_path = output_dir + output_filename + ".shp"
	processing.runalg("qgis:intersection", layer, selector_layer_name, 0, output_path)


def createNewCustomVectorLayer(name, attribute_names, attribute_types, crs=None):
	crs_param = "Polygon?crs=EPSG:4326"
	if crs is not None:
		crs_param = "Polygon?crs=EPSG:{}".format(str(crs))
	vl = QgsVectorLayer(crs_param, name, "memory")
	pr = vl.dataProvider()
	vl.startEditing()
	attribute_list = [ ]
	nattributes = len(attribute_names)
	for i in range(nattributes):
		if attribute_types[i] == "Int":
			attribute_list.append( QgsField(attribute_names[i], QVariant.Int) )
		elif attribute_types[i] == "Float":
			attribute_list.append( QgsField(attribute_names[i], QVariant.Float) )
		else:
			attribute_list.append( QgsField(attribute_names[i], QVariant.String) )
	pr.addAttributes( attribute_list )
	vl.commitChanges()
	QgsMapLayerRegistry.instance().addMapLayer(vl)
	return vl

def get_binary_grid_reference_data(valid_rect_layer, zoom, obj_layer):
    
    tl_br_lat_long = showRectangleCoordinates(valid_rect_layer)
    (width, height) = get_grid_area_size_from_bbox_lat_long(tl_br_lat_long[0][0], tl_br_lat_long[0][1], tl_br_lat_long[1][0], tl_br_lat_long[1][1], zoom)
    num_rows = height / 256
    num_cols = width / 256
    
    print "nrows {} ncols {}".format(str(num_rows), str(num_cols))
    
    reference_mat = np.zeros((num_rows, num_cols), dtype=np.uint8)
    
    
    rect_feature = valid_rect_layer.getFeatures().next()
    rect_pol = rect_feature.geometry().asPolygon()
    nelems = len(rect_pol[0])
    # get top left coordinate
    tl_rect = rect_pol[0][0]
    br_rect = rect_pol[0][2]
    
    cell_width = (br_rect.x() - tl_rect.x()) / float(num_cols)
    cell_height = (tl_rect.y() - br_rect.y()) / float(num_rows)
    
    print "cell_width, cell_height : {} {}".format(cell_width, cell_height)
    
    iter = obj_layer.getFeatures()
    for feature in iter:
        pol = feature.geometry().asPolygon()
        points = []
        try:
            points = pol[0]
        except:
            continue
        
        for point in points:
            tl_row = int( math.floor( (tl_rect.y() - point.y()) / cell_height ) )
            tl_col = int( math.floor( (point.x() - tl_rect.x()) / cell_width ) )
            if tl_row >= num_rows:
                tl_row = num_rows - 1
            
            if tl_col >= num_cols:
                tl_col = num_cols - 1
            reference_mat[tl_row, tl_col] = 1
            
    return reference_mat

def geoCoord2PixelPosition(point, top_left_x, top_left_y, pixel_size_x, pixel_size_y):
    pixPosX = int(round((point.x() - top_left_x) / pixel_size_x))
    pixPosY = int(round((top_left_y - point.y()) / pixel_size_y))
    #return QgsPoint(top_left_x + pixPosX * pixel_size_x, top_left_y - pixPosY * pixel_size_y)
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
    
    
    
    
    
    
    
    