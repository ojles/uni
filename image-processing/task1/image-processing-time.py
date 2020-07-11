import cv2
import time
import numpy
import sys

def calc_processing_time(image_path):
    image_extension = image_path.split('.')[1]

    # calculate read time
    start_time = time.time()
    image = cv2.imread(image_path)
    read_time = time.time() - start_time

    # calculate encode/decode time
    _, imageBuffer = cv2.imencode('.' + image_extension, image)
    n_try = 50
    enc_times = numpy.zeros((n_try,), dtype=numpy.float32)
    dec_times = numpy.zeros((n_try,), dtype=numpy.float32)
    for i in range(n_try):
        begin = time.time()
        _ = cv2.imencode('.' + image_extension, image)
        enc_times[i] = time.time() - begin

        begin = time.time()
        _ = cv2.imdecode(imageBuffer, 1)
        dec_times[i] = time.time() - begin



    enc_times = numpy.sort(enc_times)[1:-1]   # exclude minimum and maximum
    dev_times = numpy.sort(dec_times)[1:-1]   # exclude minimum and maximum
    encode_time = 1000 * numpy.mean(enc_times)
    decode_time = 1000 * numpy.mean(dec_times)

    # calculate write time
    start_time = time.time()
    cv2.imwrite('/tmp/temp-image.' + image_extension, image)
    write_time = time.time() - start_time

    return read_time, write_time, encode_time, decode_time


image_paths = sys.argv[1:]

print("{}\t\t{}\t\t{}\t\t{}".format('Read Time', 'Write Time', 'Encode Time', 'Decode Time'))
for image_path in image_paths:
    read_time, write_time, encode_time, decode_time = calc_processing_time(image_path)
    print("{}ms\t{}ms\t{}ms\t{}ms - {}".format(read_time, write_time, encode_time, decode_time, image_path))
