#!/bin/bash

ERR_INVALID_USAGE=1
ERR_PARAM_NOT_DIR=2

echoerr() {
    echo "$@" 1>&2;
}

print_help() {
    echo 'Usage: copy-cpp.bash SOURCE_DIR DESTINATION_DIR'
    echo 'Move all .cpp files in subdirectories of SOURCE_DIR to DESTINATION_DIR'
}

print_invalid_usage() {
    echoerr 'Invalid number of parameters!'
    echoerr "Try 'copy-cpp.bash -h' for more information."
}

if [ "$1" == '-h' ]; then
    print_help
    exit 0
fi

if [ $# != 2 ]; then
    print_invalid_usage
    exit $ERR_INVALID_USAGE
fi

if [ ! -d "$1" ]; then
    echoerr 'First parameters is not a directory!'
    exit $ERR_PARAM_NOT_DIR
fi

if [ ! -d "$2" ]; then
    echoerr 'Second parameters is not a directory!'
    exit $ERR_PARAM_NOT_DIR
fi


for subdir in $(ls -d $1/*/)
do
    for file_to_move in $(find $subdir -name '*.cpp')
    do
        mv $file_to_move $2
    done
done
