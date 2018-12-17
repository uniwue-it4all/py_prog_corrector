FROM python@sha256:5a2deb631d2526a3a6b7226917ee32dc419b95dc1c12267d4562a8c8744a7388
#FROM python:3-alpine

LABEL maintainer="b.eyselein@gmail.com"

ARG WorkDir=/data

ENV PYTHONPATH $WorkDir:$PYTHONPATH

COPY simplified_main.py extended_main.py $WorkDir/

WORKDIR $WorkDir

ENTRYPOINT timeout -t 2 -s KILL python simplified_main.py
