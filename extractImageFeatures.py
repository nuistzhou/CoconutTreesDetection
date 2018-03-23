import os
import cv2

imagePath = "/Users/nuistzhou/thesis/Kolovai-Trees-20180108/patchImages/"
imageFileName = "1.png"
imageFilePath = os.path.join(imagePath, imageFileName)
img = cv2.imread(imageFilePath)


# OpenCV  ---  SFIT
sift = cv2.xfeatures2d.SIFT_create()
featuresSIFT = sift.detectAndCompute(img, None)[1]

# OpenCV --- SURF
surf = cv2.xfeatures2d.SURF_create()
featuresSURF = surf.detectAndCompute(img, None)[1]

# OpenCv --- HOG
hog = cv2.HOGDescriptor()
featuersHOG= hog.compute(img)
