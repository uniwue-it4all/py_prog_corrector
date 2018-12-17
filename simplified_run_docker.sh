#!/usr/bin/env bash

RESULT_FILE=result.json

# Create file results.json if file not exists!
if [[ ! -f ${RESULT_FILE} ]]; then
    touch ${RESULT_FILE}
else
    > ${RESULT_FILE}
fi

# TODO: maybe check if files exist?

docker run -it --rm \
    -v $(pwd)/test_main.py:/data/test_main.py \
    -v $(pwd)/solution.py:/data/solution.py \
    -v $(pwd)/testdata.json:/data/testdata.json \
    -v $(pwd)/${RESULT_FILE}:/data/${RESULT_FILE} \
    beyselein/python_prog_tester
