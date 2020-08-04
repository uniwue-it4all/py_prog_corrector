#! /usr/bin/env bash

case $1 in
simplified)
  timeout -s KILL 2 python simplified_main.py
  ;;
unit_test)
  timeout -s KILL 4 python unit_test_main.py
  ;;
normal)
  timeout -s KILL 2 python -m unittest discover -p "*_test.py"
  ;;
*)
  echo "correction type $1 is not supported!" 1>&2
  exit 1
  ;;
esac
