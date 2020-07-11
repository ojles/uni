import numpy as np
import cv2
import time
import os
import sys


def change_file_extension(file_path, new_extension):
    return file_path.split('.')[0] + '.' + new_extension


def substract_images(first_image_path, second_image_path, output_image_path, channel='ALL'):
    first_image = cv2.imread(first_image_path)
    second_image = cv2.imread(second_image_path)
    if channel == 'ALL':
        diff = first_image - second_image
    else:
        b1, g1, r1 = cv2.split(first_image)
        b2, g2, r2 = cv2.split(second_image)
        zeros = np.zeros_like(b1)
        if channel == 'R':
            diff = r1 - r2
        elif channel == 'G':
            diff = g1 - g2
        elif channel == 'B':
            diff = b1 - b2
        else:
            raise 'Invalid channel value! (only ALL, R, G, B)'
    cv2.imwrite(output_image_path, diff)
    print(channel, np.sum((diff)))


image_path = sys.argv[1]
jpeg_image_path = change_file_extension(image_path, 'jpeg')
substract_images(image_path, jpeg_image_path, sys.argv[2])
substract_images(image_path, jpeg_image_path, sys.argv[3], 'R')
substract_images(image_path, jpeg_image_path, sys.argv[4], 'G')
substract_images(image_path, jpeg_image_path, sys.argv[5], 'B')
