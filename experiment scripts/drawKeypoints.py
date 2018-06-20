import cv2

imgPath = ''
img = cv2.imread(imgPath)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Dense key points
step_size = 5
kps = [cv2.KeyPoint(x, y, step_size) for y in range(0, gray.shape[0], step_size)
                                    for x in range(0, gray.shape[1], step_size)]

outputImgPath = ''
img=cv2.drawKeypoints(gray,kps, img)
cv2.imwrite(outputImgPath,img)

# Compute descriptors
sift = cv2.xfeatures2d.SIFT_create()
dense_feat = sift.compute(gray, kps)
