#!/usr/bin/env bash

EX=${1:?"Error: exercise folder is not defined!"}

if [[ ${EX} == */ ]]; then
  EX=${EX::-1}
fi

SOL_FILE_NAME=${EX}.py

IMG_VERSION=${IMG_VERSION:-latest}
IMG_NAME=py_simplified_prog_corrector

IMG_TAG=${IMG_NAME}:${IMG_VERSION}

# Build image?
docker build -t "${IMG_TAG}" .

# Make sure test data file exists
TEST_DATA_FILE=${EX}/test_data.json

if [[ ! -f ${TEST_DATA_FILE} ]]; then
  echo "The test data file ${TEST_DATA_FILE} does not exist!"
  exit 102
fi

# Make sure solution file exists
if [[ ! -f ${EX}/${SOL_FILE_NAME} ]]; then
  echo "The solution file ${EX}/${SOL_FILE_NAME} does not exist!"
  exit 103
fi

# Create or clear result file
RES_FILE=results/${EX}_simplified_result.json

if [[ ! -f ${RES_FILE} ]]; then
  mkdir -p results
  touch "${RES_FILE}"
else
  # shellcheck disable=SC2188
  >"${RES_FILE}"
fi

# make sure that test_main exists...
TEST_MAIN_FILE=${EX}/test_main.py

if [[ ! -f ${TEST_MAIN_FILE} ]]; then
  echo "The file test_main.py does not exist!"
  exit 101
fi

docker run -it --rm \
  -v "$(pwd)/${TEST_DATA_FILE}":/data/test_data.json \
  -v "$(pwd)/${EX}/${SOL_FILE_NAME}:/data/${SOL_FILE_NAME}" \
  -v "$(pwd)/${RES_FILE}":/data/result.json \
  -v "$(pwd)/${TEST_MAIN_FILE}":/data/test_main.py \
  ${IMG_NAME}

cat "${RES_FILE}"
