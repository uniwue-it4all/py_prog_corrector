#! /usr/bin/env bash

POSITIONALS=()
PRETTY_PRINT=""

ls -alR
#> file_list.txt

while [[ $# -gt 0 ]]; do
  case "$1" in
  -p)
    PRETTY_PRINT="$1"
    shift
    ;;
  *)
    POSITIONALS+=("$1")
    shift
    ;;
  esac
done

set -- "${POSITIONALS[@]}"

case $1 in
unit_test)
  timeout -s KILL 4 python unit_test_main.py "${PRETTY_PRINT}"
  ;;
normal)
  timeout -s KILL 4 python normal_main.py "${PRETTY_PRINT}"
  ;;
*)
  echo "correction type $1 is not supported!" 1>&2
  exit 1
  ;;
esac
