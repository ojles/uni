# Task 1

## IMPORTANT:
This code may not be the best example for encoding images and applying RLE/LZW compression.
ImageMagick is used for encoding and OpenCV is used just to calculate read/write and decode time.
Even though OpenCV could be used for encoding, though my main goal was to practice writing scripts in BASH

## Desctiption

* compress 24-bit BPM using RLE alhorothm
* convert fitrst image to TIFF and compress with LZW algorithm
* convert firhst image to JPEG using standard encoding
* compare image sizes
* calculate the image quality loss of JPEG by subtracting JPEG image from the
  original BPM image pixel by pixel
* visualize this subtraction
* calculate read, write, encode and decode time for each image format and
  compression type

## Required libraries or programs

* [ImageMagick](https://imagemagick.org)
* Python OpenCV
* `feh` or any other program to display images
