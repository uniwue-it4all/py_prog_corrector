#!/usr/bin/env sh

#echo "$@"

# pass container arguments to script file
timeout -t 2 -s KILL python main.py "$@"

# FIXME: what if timeout kills process?