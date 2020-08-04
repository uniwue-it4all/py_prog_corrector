#!/usr/bin/env bash

POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
  -t | --type)
    TYPE="$2"
    shift # past key
    shift # past value
    ;;
  *)
    POSITIONAL+=("$1")
    shift
    ;;
  esac
done

set -- "${POSITIONAL[@]}"

if [[ -z "$TYPE" ]]; then
  echo "No type was set!"
  exit 1
fi

EX=${1:?"Error: exercise name / folder is not defined!"}

if [[ ${EX} == */ ]]; then
  EX=${EX::-1}
fi

IMG_TAG=py_${TYPE}_prog_corrector:latest

# Build image
docker build -t "${IMG_TAG}" .

# check if files exist
RES_FILE=results/${TYPE}_result_${EX}.json
TEST_DATA_FILE=${EX}/${TYPE}_test_data.json

if [[ ! -f ${TEST_DATA_FILE} ]]; then
  echo "There is no test data file ${TEST_DATA_FILE}!"
  exit 102
fi

if [[ ! -f ${RES_FILE} ]]; then
  mkdir -p results
  touch "${RES_FILE}"
else
  truncate -s 0 "${RES_FILE}"
fi

# Make sure solution file and test_main exists
SOL_FILE_NAME=${EX}.py
TEST_MAIN_FILE=${EX}/test_main.py

if [[ ! -f ${EX}/${SOL_FILE_NAME} ]]; then
  echo "The solution file ${EX}/${SOL_FILE_NAME} does not exist!"
  exit 103
fi

if [[ ! -f ${TEST_MAIN_FILE} ]]; then
  echo "The file test_main.py does not exist!"
  exit 101
fi

docker run -it --rm \
  -v "$(pwd)/${TEST_DATA_FILE}:/data/test_data.json:ro" \
  -v "$(pwd)/${RES_FILE}:/data/result.json" \
  -v "$(pwd)/${EX}/${SOL_FILE_NAME}:/data/${SOL_FILE_NAME}" \
  -v "$(pwd)/${TEST_MAIN_FILE}:/data/test_main.py" \
  "${IMG_TAG}"

# cat "${RES_FILE}"
