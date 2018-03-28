#!/usr/bin/env bash

RESULT_FILE=result.json

# Create file results.json if file not exists!
if [[ ! -f ${RESULT_FILE} ]]; then
    touch ${RESULT_FILE}
fi

# TODO: maybe check if files exist?

docker run -it --rm --name test_pytest \
    -v "$PWD"/test_main.py:/data/test_main.py \
    -v "$PWD"/solution.py:/data/solution.py \
    -v "$PWD"/testdata.json:/data/testdata.json \
    -v "$PWD"/${RESULT_FILE}:/data/${RESULT_FILE} \
    beyselein/python_prog_tester
