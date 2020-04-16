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

test_invalid_number_of_param_error_code() {
    eval "$EX first second 2> /dev/null"
    assert_that $? == '1'
}

test_param_not_dir_error_code() {
    eval "$EX $0 2> /dev/null"
    assert_that $? == '2'
}

test_help_param_working() {
    eval "$EX -h > /dev/null"
    assert_that $? == '0'
}

test_calc_max_empty_dir() {
    FILE_DIR=$(mktemp -d)
    trap "rm -rf $FILE_DIR" EXIT

    EXPECTED_OUTPUT='No files found.'
    OUTPUT=$(eval "$EX $FILE_DIR")
    assert_that "$OUTPUT" == "$EXPECTED_OUTPUT"
}

test_calc_max_lines_and_max_chars() {
    FILE_DIR=$(mktemp -d)
    trap "rm -rf $FILE_DIR" EXIT

    MOST_LINES_FILE=$(mktemp -p $FILE_DIR)
    cat << EOF > $MOST_LINES_FILE
1: lskjfs
2: sldkflsdf
3: sldfjslkdf
4: sldfjslkdf
5: sldkfsS sd
6: sldkfs
7: sldkfsl sldkf
8: sldkfs
9: lwweork
10: sldkfs
EOF

    # chars amount = 9*25 + (9 - 1) = 234
    MOST_CHARS_FILE=$(mktemp -p $FILE_DIR)
    cat << EOF > $MOST_CHARS_FILE
1: lskj'sweoirq()-3'werd)
2: qpwerpoweirq()+3'cv,m)
3: sldqpweoirpq()/3'erkf)
4: sldqpweoirpq()/3'erkf)
5: sldkf,asdfbq()&3'defg)
6: 02394029341q()^3'3777)
7: sldkf,asdfbq()&3'defg)
8: sldkf,asdfbq()&3'defg)
9: sldkf,asdfbq()&3'defg)
EOF

    # chars amount = 156
    OTHER_FILE_1=$(mktemp -p $FILE_DIR)
    cat << EOF > $OTHER_FILE_1
Lorem Ipsum is simply dummy text of the printing and typesetting industry.
Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.
EOF


    EXPECTED_OUTPUT="Most lines: 10 ${MOST_LINES_FILE}
Most chars: 234 ${MOST_CHARS_FILE}"
    OUTPUT=$(eval "$EX $FILE_DIR")
    assert_that "$OUTPUT" == "$EXPECTED_OUTPUT"
}


test_invalid_number_of_param_error_code
test_param_not_dir_error_code
test_help_param_working
test_calc_max_empty_dir
test_calc_max_lines_and_max_chars
