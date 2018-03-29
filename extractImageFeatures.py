import argparse
import os
import cv2
from PIL import Image
import numpy as np
from skimage.feature import hog

#ls *.png | awk 'BEGIN{ photo=1; }{ printf "mv \"%s\" %04d.png\n", $0, photo++ }' | bash

"""
imagePath = "/media/sf_Thesis/Data/Kolovai-Trees-20180108/patchImages/lower/coco"
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
python extractImageFeatures.py ~/imagery/coco2_dataset/lower/coco/ hog ~/imagery/coco2_dataset/hog_lower_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/lower/non_coco/ hog ~/imagery/coco2_dataset/hog_lower_non_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/lower/coco/ sift ~/imagery/coco2_dataset/sift_lower_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/lower/non_coco/ sift ~/imagery/coco2_dataset/sift_lower_non_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/lower/coco/ surf ~/imagery/coco2_dataset/surf_lower_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/lower/non_coco/ surf ~/imagery/coco2_dataset/surf_lower_non_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/upper/coco/ hog ~/imagery/coco2_dataset/hog_upper_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/upper/non_coco/ hog ~/imagery/coco2_dataset/hog_upper_non_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/upper/coco/ sift ~/imagery/coco2_dataset/sift_upper_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/upper/non_coco/ sift ~/imagery/coco2_dataset/sift_upper_non_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/upper/coco/ surf ~/imagery/coco2_dataset/surf_upper_coco.npy
python extractImageFeatures.py ~/imagery/coco2_dataset/upper/non_coco/ surf ~/imagery/coco2_dataset/surf_upper_non_coco.npy

python mergeFeatureFiles.py ~/imagery/coco2_dataset/hog_lower_non_coco.npy ~/imagery/coco2_dataset/hog_lower_coco.npy ~/imagery/coco2_dataset/merged_features/hog_lower_features.npy ~/imagery/coco2_dataset/merged_features/hog_lower_labels.npy
python mergeFeatureFiles.py ~/imagery/coco2_dataset/sift_lower_non_coco.npy ~/imagery/coco2_dataset/sift_lower_coco.npy ~/imagery/coco2_dataset/merged_features/sift_lower_features.npy ~/imagery/coco2_dataset/merged_features/sift_lower_labels.npy
python mergeFeatureFiles.py ~/imagery/coco2_dataset/surf_lower_non_coco.npy ~/imagery/coco2_dataset/surf_lower_coco.npy ~/imagery/coco2_dataset/merged_features/surf_lower_features.npy ~/imagery/coco2_dataset/merged_features/surf_lower_labels.npy
python mergeFeatureFiles.py ~/imagery/coco2_dataset/hog_upper_non_coco.npy ~/imagery/coco2_dataset/hog_upper_coco.npy ~/imagery/coco2_dataset/merged_features/hog_upper_features.npy ~/imagery/coco2_dataset/merged_features/hog_upper_labels.npy
python mergeFeatureFiles.py ~/imagery/coco2_dataset/sift_upper_non_coco.npy ~/imagery/coco2_dataset/sift_upper_coco.npy ~/imagery/coco2_dataset/merged_features/sift_upper_features.npy ~/imagery/coco2_dataset/merged_features/sift_upper_labels.npy
python mergeFeatureFiles.py ~/imagery/coco2_dataset/surf_upper_non_coco.npy ~/imagery/coco2_dataset/surf_upper_coco.npy ~/imagery/coco2_dataset/merged_features/surf_upper_features.npy ~/imagery/coco2_dataset/merged_features/surf_upper_labels.npy





"""

def extract_descriptor_from_image(image, descriptor_type):
	y_center = image.shape[0]/2
	x_center = image.shape[1]/2

	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	if descriptor_type in ["sift", "surf"]:
		#print gray.shape
		if descriptor_type == "sift":
			method = cv2.SIFT(128)
		else:
			method = cv2.SURF(128)
		#print "x_center {} y_center {}".format(x_center, y_center)
		kps = [cv2.KeyPoint(x=x_center, y=y_center, _size=1)]
		kps, method_descriptor = method.compute(gray, kps)
		method_descriptor = method_descriptor[0,:]
	elif descriptor_type == "hog":
		#hog = cv2.HOGDescriptor()
		#method_descriptor = hog.compute(gray)
		method_descriptor = hog(gray, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), feature_vector=True)
	print method_descriptor.shape
	return method_descriptor

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input_dir", type=str, help="Image filename (tif)")
	parser.add_argument("descriptor_type", type=str, help="Descriptor type")
	parser.add_argument("output_features_path", type=str, help="Output png file")
	args = parser.parse_args()

	input_dir = args.input_dir
	descriptor_type = args.descriptor_type
	output_features_path = args.output_features_path
	

	filenames = os.listdir(input_dir)
	filenames.sort()
	feature_size = 128

	num_filenames = len(filenames)
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
	main()
