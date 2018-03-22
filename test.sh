#!/usr/bin/env bash

docker build -t beyselein/pytester_new .

docker run -it --rm --name test_pytest \
    -v ~/workspace/hospital/classes.py:/data/classes.py \
    -v ~/workspace/hospital/converter.py:/data/converter.py \
    -v ~/workspace/hospital/solution.py:/data/solution.py \
    -v ~/workspace/hospital/testdata.json:/data/testdata.json \
    beyselein/pytester_new