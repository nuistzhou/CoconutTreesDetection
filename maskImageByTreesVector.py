# from extractTraingSamplePatches import  *
import gdal
import numpy as np

cocoTreesUpperLayer = "cocoTreesUpperLayer"
non_cocoTreesUpperLayer = "non_cocoTreesUpperLayer"
rgbImgRaster = "rgb_image"
maskPatchSize = 90 * 2

trees_coords_array = getPointPixelCoordinates(cocoTreesUpperLayer, rgbImgRaster)
non_trees_coords_array = getPointPixelCoordinates(non_cocoTreesUpperLayer, rgbImgRaster)


rgb_image_path = '/Users/nuistzhou/thesis/Kolovai-Trees-20180108/rgb_image.tif'
rgb_image_upper= "/Users/nuistzhou/thesis/Kolovai-Trees-20180108/rgb_image_upperLayer.tif"

image = gdal.Open(rgb_image_path).ReadAsArray()
image_upper = gdal.Open(rgb_image_upper).ReadAsArray()
image = np.transpose(image, (1, 2, 0))
image_upper = np.transpose(image_upper, (1, 2, 0))

image_height = float(image.shape[0])
image_width = float(image.shape[1])
verticalHalf = float(image_upper.shape[0])

maskMatrixUpper = np.zeros((verticalHalf, image_width), np.int)
# For coconut trees
for cocoTreesCoords in trees_coords_array:
    tl_x = int(cocoTreesCoords.x() - maskPatchSize / 2)
    tl_y = int(cocoTreesCoords.y() - maskPatchSize / 2)

    br_x = tl_x + maskPatchSize
    br_y = tl_y + maskPatchSize

    tl_x = max(tl_x, 0)
    tl_y = max(tl_y, 0)
    br_x = min(br_x, image_width -1)
    br_y = min(br_y, verticalHalf -1)

    maskMatrixUpper[tl_y : br_y + 1, tl_x : br_x + 1] = 1 # Fill the box with value 1


for non_cocoTreesCoords in non_trees_coords_array:
    tl_x = int(non_cocoTreesCoords.x() - maskPatchSize / 2)
    tl_y = int(non_cocoTreesCoords.y() - maskPatchSize / 2)

    br_x = tl_x + maskPatchSize
    br_y = tl_y + maskPatchSize

    tl_x = max(tl_x, 0)
    tl_y = max(tl_y, 0)
    br_x = min(br_x, image_width -1)
    br_y = min(br_y, verticalHalf -1)

    maskMatrixUpper[tl_y : br_y + 1, tl_x : br_x + 1] = 1 # Fill the box with value 1

np.save("/Users/nuistzhou/thesis/Kolovai-Trees-20180108/maskRgbImage/upper/treesCoordsMatrix.npy", maskMatrixUpper)

