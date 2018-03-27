#!/usr/bin/env bash

# Create file results.json if file not exists!
if [[ ! -f ./results.json ]]; then
    touch results.json
fi

# TODO: maybe check if files exist?

docker run -it --rm --name test_pytest \
    -v "$PWD"/test_main.py:/data/test_main.py \
    -v "$PWD"/solution.py:/data/solution.py \
    -v "$PWD"/testdata.json:/data/testdata.json \
    -v "$PWD"/results.json:/data/results.json \
    beyselein/python_prog_tester
