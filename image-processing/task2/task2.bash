#!/bin/bash

#
# Resources:
# - https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_histograms/py_histogram_equalization/py_histogram_equalization.html
# - https://stackoverflow.com/questions/34126272/histogram-equalization-without-opencv
# - https://habr.com/ru/post/128753/
# - https://prateekvjoshi.com/2013/11/22/histogram-equalization-of-rgb-images/
# - https://en.wikipedia.org/wiki/Roberts_cross
#

if [ ! "$#" == "1" ]; then
    echo "Invalid number of parameters!"
    echo "Usage: ./task2.bash <IMAGE>"
    exit 1
fi


IMG_NAME=$(echo ${1} | sed 's/\(.*\)\.\(.*\)/\1/')
IMG_EXT=$(echo ${1} | sed 's/\(.*\)\.\(.*\)/\2/')
IMG=${IMG_NAME}.${IMG_EXT}
IMG_NO_EQ=${IMG_NAME}-no-eq.jpg
IMG_EQ=${IMG_NAME}-eq.jpg
IMG_ROBERTS_OP=${IMG_NAME}-roberts-op.jpg
IMG_PREWITT_OP=${IMG_NAME}-prewitt-op.jpg
IMG_SOBEL_OP=${IMG_NAME}-sobel-op.jpg

put_histogram_on_image() {
    TEMP_HIST=temp-hist.jpg
    convert $1 -define histogram:unique-colors=false histogram:$TEMP_HIST
    convert $1 $TEMP_HIST -compose over -gravity SouthEast -composite $1
    rm $TEMP_HIST
}


# preserve the original image
cp $IMG $IMG_NO_EQ


# run equalization
python equalize-histogram.py $IMG_NO_EQ $IMG_EQ


# put histograms on non-equalized and equalized images
put_histogram_on_image $IMG_NO_EQ
put_histogram_on_image $IMG_EQ


# apply sobel operator
python roberts.py $IMG $IMG_ROBERTS_OP
#convert $IMG -define convolve:scale='50%!' -bias 50% -morphology Convolve Roberts:45 $IMG_ROBERTS_OP
python sobel.py $IMG $IMG_SOBEL_OP
#convert $IMG -define convolve:scale='50%!' -bias 50% -morphology Convolve Sobel $IMG_SOBEL_OP
python prewitt.py $IMG $IMG_PREWITT_OP
#convert $IMG -define convolve:scale='50%!' -bias 50% -morphology Convolve Prewitt $IMG_PREWITT_OP


# show images
feh --scale-down --auto-zoom $IMG_NO_EQ $IMG_EQ $IMG_ROBERTS_OP $IMG_PREWITT_OP $IMG_SOBEL_OP
