# from extractTraingSamplePatches import  *
import gdal
import numpy as np

cocoTreesUpperLayer = "cocoTreesUpperLayer"
non_cocoTreesUpperLayer = "non_cocoTreesUpperLayer"
cocoTreesLowerLayer = "cocoTreesLowerLayer"
non_cocoTreesLowerLayer = "non_cocoTreesUpperLayer"

rgbImgRaster = "rgb_image"
maskPatchSize = 90 * 2  # Double patch size to avoid overlapping between patch samples

upper_coco_coords_array = getPointPixelCoordinates(cocoTreesUpperLayer, rgbImgRaster)
upper_non_coco_coords_array = getPointPixelCoordinates(non_cocoTreesUpperLayer, rgbImgRaster)
lower_coco_coords_array = getPointPixelCoordinates(cocoTreesLowerLayer, rgbImgRaster)
lower_non_coco_coords_array = getPointPixelCoordinates(non_cocoTreesLowerLayer, rgbImgRaster)

rgb_image_path = '/Users/ping/thesis/data/rgb_image.tif'
rgb_image_upper = "/Users/ping/thesis/data/rgb_image_upperLayer.tif"

image = gdal.Open(rgb_image_path).ReadAsArray()
image_upper = gdal.Open(rgb_image_upper).ReadAsArray()
image = np.transpose(image, (1, 2, 0))
image_upper = np.transpose(image_upper, (1, 2, 0))

image_height = float(image.shape[0])
image_width = float(image.shape[1])
verticalHalf = float(image_upper.shape[0])

maskMatrixUpper = np.zeros((verticalHalf, image_width), np.int)  # Set the default filling value as 0 for unmasking area
maskMatrixLower = np.zeros((image_height - verticalHalf, image_width), np.int)

## Upper layer
# Coconut trees masking
for cocoTreesCoords in upper_coco_coords_array:
    tl_x = int(cocoTreesCoords.x() - maskPatchSize / 2)  # tl : top-left
    tl_y = int(cocoTreesCoords.y() - maskPatchSize / 2)

    br_x = tl_x + maskPatchSize  # br: bottom-right
    br_y = tl_y + maskPatchSize

    # Replace with boundary when beyond
    tl_x = max(tl_x, 0)
    tl_y = max(tl_y, 0)
    br_x = min(br_x, image_width - 1)
    br_y = min(br_y, verticalHalf - 1)

    maskMatrixUpper[tl_y: br_y + 1, tl_x: br_x + 1] = 1  # Fill the box with value 1 as a mask

# Non_coconut trees masking
for non_cocoTreesCoords in upper_non_coco_coords_array:
    tl_x = int(non_cocoTreesCoords.x() - maskPatchSize / 2)
    tl_y = int(non_cocoTreesCoords.y() - maskPatchSize / 2)

    br_x = tl_x + maskPatchSize
    br_y = tl_y + maskPatchSize

    # Replace with boundary when beyond
    tl_x = max(tl_x, 0)
    tl_y = max(tl_y, 0)
    br_x = min(br_x, image_width - 1)
    br_y = min(br_y, verticalHalf - 1)

    maskMatrixUpper[tl_y: br_y + 1, tl_x: br_x + 1] = 1  # Fill the box with value 1 as a mask

maskMatrixUpper = np.multiply(maskMatrixUpper, 255)  # To make the matrix value as either 0 or 255 for visualization
np.save("/Users/ping/thesis/data/datamaskRgbImage/upper/treesMaskMatrix.npy", maskMatrixUpper)

## Lower layer
# coconut trees
for cocoTreesCoords in lower_coco_coords_array:
    tl_x = int(cocoTreesCoords.x() - maskPatchSize / 2)  # tl : top-left
    tl_y = int(cocoTreesCoords.y() - verticalHalf - maskPatchSize / 2)

    br_x = tl_x + maskPatchSize  # br: bottom-right
    br_y = tl_y + maskPatchSize

    # Replace with boundary when beyond
    tl_x = max(tl_x, 0)
    tl_y = max(tl_y, 0)
    br_x = min(br_x, image_width - 1)
    br_y = min(br_y, image_height - 1)

    maskMatrixLower[tl_y: br_y + 1, tl_x: br_x + 1] = 1  # Fill the box with value 1 as a mask

# non-coconut trees
for non_cocoTreesCoords in lower_non_coco_coords_array:
    tl_x = int(non_cocoTreesCoords.x() - maskPatchSize / 2)
    tl_y = int(non_cocoTreesCoords.y() - verticalHalf - maskPatchSize / 2)

    br_x = tl_x + maskPatchSize
    br_y = tl_y + maskPatchSize

    # Replace with boundary when beyond
    tl_x = max(tl_x, 0)
    tl_y = max(tl_y, 0)
    br_x = min(br_x, image_width - 1)
    br_y = min(br_y, image_height - 1)

    maskMatrixLower[tl_y: br_y + 1, tl_x: br_x + 1] = 1  # Fill the box with value 1 as a mask

maskMatrixLower = np.multiply(maskMatrixLower, 255)  # To make the matrix value as either 0 or 255 for visualization
np.save("/Users/ping/thesis/data/maskRgbImage/lower/treesMaskMatrix.npy", maskMatrixLower)
