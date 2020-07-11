import sys
import cv2 
import numpy as np 


input_image_path = sys.argv[1]
output_image_path = sys.argv[2]

image = cv2.imread(input_image_path)

kernelx = np.array([
    [1, 0],
    [0, -1]])
kernely = np.array([
    [0, 1],
    [-1, 0]])

robertsx = cv2.filter2D(image, -1, kernelx)
robertsy = cv2.filter2D(image, -1, kernely)
roberts = robertsx + robertsy

cv2.imwrite(output_image_path, roberts)
