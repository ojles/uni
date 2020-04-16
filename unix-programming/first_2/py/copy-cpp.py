#!/usr/bin/python3

import sys
import os

ERR_INVALID_USAGE = 1
ERR_PARAM_NOT_DIR = 2

def eprint(*args):
    print(*args, file=sys.stderr)


if len(sys.argv) >= 2 and sys.argv[1] == '-h':
    print('Usage: copy-cpp.py SOURCE_DIR DESTINATION_DIR')
    print('Move all .cpp files in subdirectories of SOURCE_DIR to DESTINATION_DIR')
    sys.exit(0)

if len(sys.argv) != 3:
    eprint('Invalid number of parameters!')
    eprint("Try 'copy-cpp.py -h' for more information.")
    sys.exit(ERR_INVALID_USAGE)

if not os.path.isdir(sys.argv[1]):
    eprint('First parameters is not a directory!')
    sys.exit(ERR_PARAM_NOT_DIR)

if not os.path.isdir(sys.argv[2]):
    eprint('Second parameters is not a directory!')
    sys.exit(ERR_PARAM_NOT_DIR)


sourceDir = sys.argv[1]
destinationDir = sys.argv[2]


for subdir in os.listdir(sourceDir):
    subdirFullPath = os.path.join(sourceDir, subdir)
    if  not os.path.isdir(subdirFullPath):
        continue

    for root, dirs, files in os.walk(subdirFullPath):
        for file in files:
            if file.endswith('.cpp'):
                os.rename(os.path.join(root, file), os.path.join(destinationDir, file))
