import sys
import cv2 
import numpy as np 

# https://stackoverflow.com/questions/15007304/histogram-equalization-not-working-on-color-image-opencv
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_histograms/py_histogram_equalization/py_histogram_equalization.html

input_image_path = sys.argv[1]
output_image_path = sys.argv[2]

image = cv2.imread(input_image_path)
ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
channels = cv2.split(ycrcb)
cv2.equalizeHist(channels[0], channels[0])
cv2.merge(channels, ycrcb)
cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, image)
cv2.imwrite(output_image_path, image)
