#!/usr/bin/env bash

SOL_FILE=solution.py

if [[ "$1" = "--extended" ]]
then
    RES_FILE=docker_extended_result.json
    ADDITIONAL_MOUNT=""
else
    RES_FILE=docker_simplified_result.json
    ADDITIONAL_MOUNT="-v $(pwd)/test_main.py:/data/test_main.py"

    # make sure that test_main exists...
    if [[ ! -f test_main.py ]]
    then
        echo "The file test_main.py does not exist!"
        exit 101
    fi
fi

TEST_DATA_FILE=unified_test_data.json


# Make sure test data file exists
if [[ ! -f ${TEST_DATA_FILE} ]]
then
    echo "The test data file ${TEST_DATA_FILE} does not exist!"
    exit 102
fi

# Make sure solution file exists
if [[ ! -f ${SOL_FILE} ]]
then
    echo "The solution file ${SOL_FILE} does not exist!"
    exit 103
fi

# Create or clear result file
if [[ ! -f ${RES_FILE} ]]
then
    touch ${RES_FILE}
else
    > ${RES_FILE}
fi

docker run -it --rm \
    -v $(pwd)/${TEST_DATA_FILE}:/data/test_data.json \
    -v $(pwd)/${SOL_FILE}:/data/solution.py \
    -v $(pwd)/${RES_FILE}:/data/result.json \
    ${ADDITIONAL_MOUNT} prog_tester_new $1