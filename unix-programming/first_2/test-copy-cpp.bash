#!/bin/bash

if [ $# != '1' ]; then
    echo 'Error: invalid number of parameters!'
    echo 'Please specify executable to test'
    exit 1
fi

EX=./$1

assert_that() {
    test "$1" "$2" "$3"
    if [ $? == '0' ]; then
        echo " >> PASSED: ${FUNCNAME[1]}"
    else
        echo " >> FAILED: ${FUNCNAME[1]}"
    fi
}

test_help_param_working() {
    eval "$EX -h > /dev/null"
    assert_that $? == '0'
}

test_invalid_number_of_param_error_code() {
    eval "$EX first 2> /dev/null"
    assert_that $? == '1'
}

test_first_param_not_dir_error_code() {
    eval "$EX $0 '/' 2> /dev/null"
    assert_that $? == '2'
}

test_second_param_not_dir_error_code() {
    eval "$EX '/' $0 2> /dev/null"
    assert_that $? == '2'
}


test_calc_max_empty_dir() {
    FILE_DIR=$(mktemp -d)
    trap "rm -rf $FILE_DIR" EXIT

    EXPECTED_OUTPUT='No files found.'
    OUTPUT=$(eval "$EX $FILE_DIR")
    assert_that "$OUTPUT" == "$EXPECTED_OUTPUT"
}

test_move_cpp_files() {
    DIR=$(mktemp -d)
    DEST_DIR=$(mktemp -d)
    trap "rm -rf $DIR $DEST_DIR" EXIT

    FILE_1=$(mktemp -p $DIR file1.XXXXX.cpp)

    SUBDIR_1=$(mktemp -p $DIR -d)
    FILE_2=$(mktemp -p $SUBDIR_1 file2.XXXXX.cpp)

    SUBDIR_2=$(mktemp -p $DIR -d)
    FILE_3=$(mktemp -p $SUBDIR_2 file3.XXXXX.cpp)
    FILE_4=$(mktemp -p $SUBDIR_2 file4.XXXXX.cpp)

    eval "$EX $DIR $DEST_DIR"
    if [ -e "$DEST_DIR/$(basename $FILE_2)" ] && [ -e "$DEST_DIR/$(basename $FILE_3)" ] && [ -e "$DEST_DIR/$(basename $FILE_4)" ]; then
        echo " >> PASSED: ${FUNCNAME[0]}"
    else
        echo " >> FAILED: ${FUNCNAME[0]}"
    fi
}


test_help_param_working
test_invalid_number_of_param_error_code
test_first_param_not_dir_error_code
test_second_param_not_dir_error_code
test_move_cpp_files
