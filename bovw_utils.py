import os
import numpy as np
from skimage.feature import hog
import cv2

def extract_local_descriptors(img_dir):
    list_decriptors = []
    list_img_labels = []
    # set descriptor method
    # desc_method = cv2.SURF(1000)

    desc_method = cv2.xfeatures2d.SIFT_create()
    # desc_method = cv2.xfeatures2d.SURF_create(400, extended=True)

    # get image filenames inside the image directory input
    img_files = [ f for f in os.listdir(img_dir)]
    img_files.sort()

    # Dense sift with block size of 5 pixels
    step_size = 5

    for img_file in img_files:
        arr_filename = img_file.split('_') # asuming that the format is class_imagenumber.jpg
        # obtain label
        label = int(arr_filename[0])
        img_path = img_dir + img_file
        img = cv2.imread(img_path, 0)

        # Dense SIFT
        kps = [cv2.KeyPoint(x, y, step_size) for y in range(0, img.shape[0], step_size)
              for x in range(0, img.shape[1], step_size)]
        kps, descriptors = desc_method.compute(img, kps)

        # Normal SIFT
        # kps, descriptors = desc_method.detectAndCompute(img, None)

        # HOG
        # descriptors = hog(img, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1),
        #                         feature_vector=True)

        list_decriptors.append(descriptors)
        list_img_labels.append(label)
        print "img_path {} npoints {}".format(img_path, descriptors.shape[0])

    return list_decriptors, list_img_labels


def extract_local_descriptor_ImageArrayList(imgArrayList):
    step_size = 15
    labels = list()
    descriptorList = list()
    desc_method = cv2.xfeatures2d.SIFT_create()
    print "Generating feature descriptors..."
    for imgArray in imgArrayList:
        kps = [cv2.KeyPoint(x, y, step_size) for y in range(0, imgArray.shape[0], step_size)
               for x in range(0, imgArray.shape[1], step_size)]
        kps, descriptors = desc_method.compute(imgArray, kps)
        labels.append(1)
        descriptorList.append(descriptors)

    return descriptorList, labels

def extract_local_descriptor_ImageArray(imgArray):
    step_size = 15
    desc_method = cv2.xfeatures2d.SIFT_create()
    kps = [cv2.KeyPoint(x, y, step_size) for y in range(0, imgArray.shape[0], step_size)
           for x in range(0, imgArray.shape[1], step_size)]
    kps, descriptors = desc_method.compute(imgArray, kps)

    return descriptors


