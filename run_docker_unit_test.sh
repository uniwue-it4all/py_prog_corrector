#!/usr/bin/env bash

POSITIONALS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
  -t | --type)
    value="$2"
    case $value in
    simplified)
      TYPE="$value"
      ;;
    unit_test)
      TYPE="$value"
      ;;
    normal)
      TYPE="$value"
      ;;
    *)
      echo "Type $2 is not defined!" 1>&2
      exit 2
      ;;
    esac
    shift # past key
    shift # past value
    ;;
  *)
    POSITIONALS+=("$1")
    shift
    ;;
  esac
done

set -- "${POSITIONALS[@]}"

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

# TODO: other files
case $TYPE in
simplified)
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

  MOUNTS="\
  -v $(pwd)/${EX}/${SOL_FILE_NAME}:/data/${SOL_FILE_NAME} \
  -v $(pwd)/${TEST_MAIN_FILE}:/data/test_main.py"
  ;;
unit_test)
  MOUNTS="\
  -v $(pwd)/${EX}/:/data/${EX}"
  ;;
normal)
  MOUNTS=""
  ;;
esac

docker_command="
docker run -it --rm \
  -v $(pwd)/${TEST_DATA_FILE}:/data/test_data.json:ro \
  -v $(pwd)/${RES_FILE}:/data/result.json ${MOUNTS} \
  ${IMG_TAG}
"

echo "$docker_command"

eval "$docker_command"

# cat "${RES_FILE}"
