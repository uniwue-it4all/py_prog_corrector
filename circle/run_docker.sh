#!/usr/bin/env bash

if [[ "$1" = "--extended" ]]
then
    TEST_DATA_FILE=extended_test_data.json
    RES_FILE=docker_extended_result.json
else
    TEST_DATA_FILE=simplified_test_data.json
    RES_FILE=docker_simplified_result.json
fi

if [[ ! -f ${RES_FILE} ]]
then
    touch ${RES_FILE}
else
    > ${RES_FILE}
fi

docker run -it --rm \
    -v $(pwd)/${TEST_DATA_FILE}:/data/test_data.json \
    -v $(pwd)/solution.py:/data/solution.py \
    -v $(pwd)/test_main.py:/data/test_main.py \
    -v $(pwd)/${RES_FILE}:/data/result.json \
    prog_tester_new $1