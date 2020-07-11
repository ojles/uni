#!/bin/bash

#
# IMPORTANT:
#  This code may not be the best example for encoding images and applying RLE/LZW compression.
#  ImageMagick is used for encoding and OpenCV is used just to calculate read/write and decode time.
#  Even though OpenCV could be used for encoding, though my main goal was to practice writing scripts in BASH
#

IMG=dog
IMG_BMP=${IMG}.bmp
IMG_BMP_8BIT=${IMG}-8.bmp
IMG_BMP_8BIT_RLE=${IMG}-8-rle.bmp
IMG_TIFF_LZW=${IMG}-lzw.tiff
IMG_JPEG=${IMG}.jpeg
IMG_DIFF=${IMG}-diff.bmp
IMG_DIFF_RED=${IMG}-diff-red.bmp
IMG_DIFF_GREEN=${IMG}-diff-green.bmp
IMG_DIFF_BLUE=${IMG}-diff-blue.bmp


_time() {
    \time -f '(%es)' ${1} > /dev/null
}

file_size() {
    du -h ${1}
}

compress_images() {
    printf 'Compressing 24-bit BMP using RLE algorithm... (fail)\n'
    echo "    ERROR: Seems like it's not possible to compress 24-bit BPM file. More info here:"
    echo '        - http://www.imagemagick.org/discourse-server/viewtopic.php?t=33902'
    echo '        - https://en.wikipedia.org/wiki/BMP_file_format#Compression'
    printf '    Converting 24-bit BMP to 8-bit indexed BMP... '
    _time "convert ${IMG_BMP} -compress NONE -depth 8 -type palette ${IMG_BMP_8BIT}"
    printf '    Compressing 8-bit BMP using RLE algorithm... '
    _time "convert ${IMG_BMP_8BIT} -compress RLE ${IMG_BMP_8BIT_RLE}"
    printf 'Converting BMP to TIFF and compressing using LZW algorithm... '
    _time "convert ${IMG_BMP} -compress LZW ${IMG_TIFF_LZW}"
    printf 'Converting BMP to JPEG using Standard Encoding... '
    _time "convert ${IMG_BMP} ${IMG_JPEG}"
}

print_file_sizes() {
    echo 'File size comparison:'
    echo -e "    24-bit uncompressed BMP: \t$(file_size ${IMG_BMP})"
    echo -e "    8-bit uncompressed BMP: \t$(file_size ${IMG_BMP_8BIT})"
    echo -e "    8-bit RLE compressed BMP: \t$(file_size ${IMG_BMP_8BIT_RLE})"
    echo -e "    8-bit LZW compressed TIFF: \t$(file_size ${IMG_TIFF_LZW})"
    echo -e "    8-bit JPEG in JFIF format: \t$(file_size ${IMG_JPEG})"
}

diff_images() {
    echo 'Computing the loss of JPEG compression...'
    python diff-image.py $IMG_BMP $IMG_DIFF $IMG_DIFF_RED $IMG_DIFF_GREEN $IMG_DIFF_BLUE

    # Display result.
    # Replace 'feh' with your default image viewer.
    feh $IMG_DIFF $IMG_DIFF_RED $IMG_DIFF_GREEN $IMG_DIFF_BLUE
}

calculate_read_write_decode_time() {
    python image-processing-time.py $IMG_BMP $IMG_BMP_8BIT $IMG_BMP_8BIT_RLE $IMG_TIFF_LZW $IMG_JPEG
}


compress_images
echo ''
print_file_sizes
echo ''
diff_images
echo ''
calculate_read_write_decode_time
