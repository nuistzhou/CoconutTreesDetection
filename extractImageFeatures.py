import argparse
import os
import cv2
from PIL import Image
import numpy as np
from skimage.feature import hog
from config import Parameters

"""
rename filename
ls *.png | awk 'BEGIN{ photo=1; }{ printf "mv \"%s\" %04d.png\n", $0, photo++ }' | bash
"""

"""
imagePath = "/Users/ping/thesis/data/patchImages/lower/coco"
imageFileName = "1.png"
imageFilePath = os.path.join(imagePath, imageFileName)
img = cv2.imread(imageFilePath)


# OpenCV  ---  SFIT
sift = cv2.xfeatures2d.SIFT_create()
featuresSIFT = sift.detectAndCompute(img, None)[1]  # Dimension of (175, 128)

# OpenCV --- SURF
surf = cv2.xfeatures2d.SURF_create()
featuresSURF = surf.detectAndCompute(img, None)[1]  # Dimension of (31, 64)

# # OpenCv --- HOG
# hog = cv2.HOGDescriptor()
# featuersHOG= hog.compute(img)
"""

"""
python extractImageFeatures.py ~/patchImages/lower/coco/ hog ~/featureDescriptors/hog_lower_coco.npy
python extractImageFeatures.py ~/patchImages/lower/non_coco/ hog ~/featureDescriptors/hog_lower_non_coco.npy
python extractImageFeatures.py ~/patchImages/lower/coco/ sift ~/featureDescriptors/sift_lower_coco.npy
python extractImageFeatures.py ~/patchImages/lower/non_coco/ sift ~/featureDescriptors/sift_lower_non_coco.npy
python extractImageFeatures.py ~/patchImages/lower/coco/ surf ~/featureDescriptors/surf_lower_coco.npy
python extractImageFeatures.py ~/patchImages/lower/non_coco/ surf ~/featureDescriptors/surf_lower_non_coco.npy
python extractImageFeatures.py ~/patchImages/upper/coco/ hog ~/featureDescriptors/hog_upper_coco.npy
python extractImageFeatures.py ~/patchImages/upper/non_coco/ hog ~/featureDescriptors/hog_upper_non_coco.npy
python extractImageFeatures.py ~/patchImages/upper/coco/ sift ~/featureDescriptors/sift_upper_coco.npy
python extractImageFeatures.py ~/patchImages/upper/non_coco/ sift ~/featureDescriptors/sift_upper_non_coco.npy
python extractImageFeatures.py ~/patchImages/upper/coco/ surf ~/featureDescriptors/surf_upper_coco.npy
python extractImageFeatures.py ~/patchImages/upper/non_coco/ surf ~/featureDescriptors/surf_upper_non_coco.npy

"""


def extract_descriptor_from_image(image, descriptor_type):
    y_center = image.shape[0] / 2
    x_center = image.shape[1] / 2

    method_descriptor = None
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    if descriptor_type in ["sift", "surf"]:
        if descriptor_type == "sift":
            method = cv2.xfeatures2d.SIFT_create(400)
        else:
            # Use extended 128-element descriptors, default SURF descriptor only have 64 dimensions
            method = cv2.xfeatures2d.SURF_create(400, extended=True)
        kps = [cv2.KeyPoint(x=x_center, y=y_center, _size=1)]
        kps, method_descriptor = method.compute(gray, kps)
        method_descriptor = method_descriptor[0, :]
    elif descriptor_type == "hog":
        method_descriptor = hog(gray, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1),
                                feature_vector=True)
    return method_descriptor


def main(input_dir, descriptor_type, output_features_path):
    #----------------input paras from command line
    # parser = argparse.ArgumentParser()
    # parser.add_argument("input_dir", type=str, help="Image filename (tif)")
    # parser.add_argument("descriptor_type", type=str, help="Descriptor type")
    # parser.add_argument("output_features_path", type=str, help="Output png file")
    # args = parser.parse_args()
    #
    # input_dir = args.input_dir
    # descriptor_type = args.descriptor_type
    # output_features_path = args.output_features_path
    #----------------------------------
    input_dir = os.path.join(Parameters.dataPath, input_dir)
    output_features_path = os.path.join(Parameters.dataPath, output_features_path)
    filenames = os.listdir(input_dir)
    filenames.sort()
    feature_size = 128

    features = []
    for i, filename in enumerate(filenames):
        fullpath = "{}{}".format(input_dir, filename)
        img_pil = Image.open(fullpath)
        img = np.array(img_pil)

        descriptor = extract_descriptor_from_image(img, descriptor_type)

        features.append(descriptor)

    features = np.array(features)

    np.save(output_features_path, features)


if __name__ == '__main__':
    main("patchImages/lower/coco/", "hog","featureDescriptors/hog_lower_coco.npy")
    main("patchImages/lower/non_coco/", "hog", "featureDescriptors/hog_lower_non_coco.npy")
    main("patchImages/lower/coco/", "sift", "featureDescriptors/sift_lower_coco.npy")
    main("patchImages/lower/non_coco/", "sift", "featureDescriptors/sift_lower_non_coco.npy")
    main("patchImages/lower/coco/", "surf", "featureDescriptors/surf_lower_coco.npy")
    main("patchImages/lower/non_coco/", "surf", "featureDescriptors/surf_lower_non_coco.npy")
    main("patchImages/upper/coco/", "hog", "featureDescriptors/hog_upper_coco.npy")
    main("patchImages/upper/non_coco/", "hog", "featureDescriptors/hog_upper_non_coco.npy")
    main("patchImages/upper/coco/", "sift", "featureDescriptors/sift_upper_coco.npy")
    main("patchImages/upper/non_coco/", "sift", "featureDescriptors/sift_upper_non_coco.npy")
    main("patchImages/upper/coco/", "surf", "featureDescriptors/surf_upper_coco.npy")
    main("patchImages/upper/non_coco/", "surf", "featureDescriptors/surf_upper_non_coco.npy")

