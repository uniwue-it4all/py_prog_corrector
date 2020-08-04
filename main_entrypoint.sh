#! /usr/bin/env bash

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

echo "$TYPE"

echo "$1"
