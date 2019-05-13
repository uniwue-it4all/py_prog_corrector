FROM python:3-alpine

RUN pip install --upgrade pip jsonschema

LABEL maintainer="b.eyselein@gmail.com"

ARG WorkDir=/data

ENV PYTHONPATH $WorkDir:$PYTHONPATH

COPY main.py simplified_main.py test_data.schema.json $WorkDir/

WORKDIR $WorkDir

ENTRYPOINT timeout -t 2 -s KILL python main.py