#!/usr/bin/env bash

SOL_FILE=circle.py
RESULT_FILE=result.json

docker build -t prog_single_tester ./.

if [[ ! -f ${RESULT_FILE} ]]
then
    touch ${RESULT_FILE}
else
    > ${RESULT_FILE}
fi

docker run -it --rm \
    -v $(pwd)/testdata.json:/data/testdata.json \
    -v $(pwd)/${RESULT_FILE}:/data/${RESULT_FILE} \
    -v $(pwd)/${SOL_FILE}:/data/${SOL_FILE} \
    prog_single_tester