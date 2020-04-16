#!/usr/bin/python3

import sys
import os


ERR_INVALID_PARAM_NUMBER = 1
ERR_PARAM_NOT_DIR = 2

def eprint(*args):
    print(*args, file=sys.stderr)


def fileLines(filePath):
    return sum(1 for line in open(filePath))

def fileChars(filePath):
    return sum(len(line) for line in open(filePath))

class FileInfo(object):
    pass


if len(sys.argv) != 2:
    eprint('Invalid number of parameters!')
    sys.exit(ERR_INVALID_PARAM_NUMBER)

if sys.argv[1] == '-h':
    print('Usage: search-files.bash DIRECTORY')
    print('Searches for files with most lines and most characters')
    sys.exit(0)

if not os.path.isdir(sys.argv[1]):
    eprint("'$1' is not a directory!")
    sys.exit(ERR_PARAM_NOT_DIR)



mostLines = FileInfo()
mostLines.path = None
mostLines.amount = 0

mostChars = FileInfo()
mostChars.path = None
mostChars.amount = 0

for root, dirs, files in os.walk(sys.argv[1]):
    for fileName in files:
        filePath = os.path.join(root, fileName)
        linesAmount = fileLines(filePath)
        charsAmount = fileChars(filePath)

        if linesAmount > mostLines.amount:
            mostLines.amount = linesAmount
            mostLines.path = filePath

        if charsAmount > mostChars.amount:
            mostChars.amount = charsAmount
            mostChars.path = filePath


if mostLines.path is None and mostChars.path is None:
    print("No files found.")
else:
    print("Most lines: {0} {1}".format(mostLines.amount, mostLines.path))
    print("Most chars: {0} {1}".format(mostChars.amount, mostChars.path))
