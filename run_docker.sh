#!/usr/bin/env bash

EX=${1:?"Error: exercise folder is not defined!"}

SOL_FILE=${EX}/solution.py

IMG_NAME=beyselein/python_prog_tester:simple

docker build -t ${IMG_NAME} .

# Make sure test data file exists
TEST_DATA_FILE=${EX}/test_data.json
if [[ ! -f ${TEST_DATA_FILE} ]]; then
    echo "The test data file ${TEST_DATA_FILE} does not exist!"
    exit 102
fi

# Make sure solution file exists
if [[ ! -f ${SOL_FILE} ]]; then
    echo "The solution file ${SOL_FILE} does not exist!"
    exit 103
fi

# Create or clear result file
RES_FILE=results/${EX}_simplified_result.json
if [[ ! -f ${RES_FILE} ]]; then
    mkdir results
    touch ${RES_FILE}
else
    > ${RES_FILE}
fi

# make sure that test_main exists...
TEST_MAIN_FILE=${EX}/test_main.py
if [[ ! -f ${TEST_MAIN_FILE} ]]; then
    echo "The file test_main.py does not exist!"
    exit 101
fi

docker run -it --rm \
    -v $(pwd)/${TEST_DATA_FILE}:/data/test_data.json \
    -v $(pwd)/${SOL_FILE}:/data/solution.py \
    -v $(pwd)/${RES_FILE}:/data/result.json \
    -v $(pwd)/${TEST_MAIN_FILE}:/data/test_main.py \
    ${IMG_NAME}