import os
import cv2

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
