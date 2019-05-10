#!/usr/bin/env bash

EX=${1:-ggt}

SOL_FILE=${EX}/solution.py

IMG_NAME=beyselein/python_prog_tester:extended

if [[ "$2" = "--extended" ]]; then
    RES_FILE=results/${EX}_extended_result.json
    ADDITIONAL_MOUNT="-v $(pwd)/${EX}/extended_tests.py:/data/extended_tests.py"

    # make sure tests_file exists
    if [[ ! -f ${EX}/extended_tests.py ]]; then
        echo "The file extended_tests.py does not exist!"
        exit 101
    fi

else
    RES_FILE=results/${EX}_simplified_result.json
    ADDITIONAL_MOUNT="-v $(pwd)/${EX}/test_main.py:/data/test_main.py"

    # make sure that test_main exists...
    if [[ ! -f ${EX}/test_main.py ]]; then
        echo "The file test_main.py does not exist!"
        exit 101
    fi
fi

TEST_DATA_FILE=${EX}/unified_test_data.json

# Make sure test data file exists
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
if [[ ! -f ${RES_FILE} ]]; then
    touch ${RES_FILE}
else
    > ${RES_FILE}
fi

docker run -it --rm \
    -v $(pwd)/${TEST_DATA_FILE}:/data/test_data.json \
    -v $(pwd)/${SOL_FILE}:/data/solution.py \
    -v $(pwd)/${RES_FILE}:/data/result.json \
    ${ADDITIONAL_MOUNT} ${IMG_NAME} $2