#!/bin/bash

ERR_INVALID_PARAM_NUMBER=1
ERR_PARAM_NOT_DIR=2

echoerr() {
    echo "$@" 1>&2;
}

if [ "$1" == '-h' ]; then
    echo 'Usage: search-files.bash DIRECTORY'
    echo 'Searches for files with most lines and most characters'
    exit 0
fi

if [ $# != 1 ]; then
    echoerr 'Invalid number of parameters!'
    echoerr "Try 'search-files -h' for more information."
    exit $ERR_INVALID_PARAM_NUMBER
fi

if [ ! -d $1 ]; then
    echoerr "'$1' is not a directory!"
    exit $ERR_PARAM_NOT_DIR
fi


MOST_LINES_RES=$(find $1 -type f -exec wc -l '{}' \; | sort -rn | head -n 1)
MOST_CHARS_RES=$(find $1 -type f -exec wc -m '{}' \; | sort -rn | head -n 1)

if [ "$MOST_LINES_RES" == '' ] && [ "$MOST_CHARS_RES" == '' ]; then
    echo 'No files found.'
else
    echo "Most lines: ${MOST_LINES_RES}"
    echo "Most chars: ${MOST_CHARS_RES}"
fi
