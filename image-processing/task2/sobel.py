import sys
import cv2 
import numpy as np 


input_image_path = sys.argv[1]
output_image_path = sys.argv[2]

ddepth = -1
ksize = 3

image = cv2.imread(input_image_path)
grad_x = cv2.Sobel(image, ddepth, 1, 0, ksize=ksize, borderType=cv2.BORDER_DEFAULT)
grad_y = cv2.Sobel(image, ddepth, 0, 1, ksize=ksize, borderType=cv2.BORDER_DEFAULT)

#abs_grad_x = cv2.convertScaleAbs(grad_x)
#abs_grad_y = cv2.convertScaleAbs(grad_y)
#grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

cv2.imwrite(output_image_path, grad_x + grad_y)
