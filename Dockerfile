FROM python:3-alpine

RUN pip install --upgrade pip jsonschema

LABEL maintainer="b.eyselein@gmail.com"

ARG WORKDIR=/data

ENV PYTHONPATH $WORKDIR:$PYTHONPATH

COPY main.py simplified_main.py test_data.schema.json $WORKDIR/

WORKDIR $WORKDIR

ENTRYPOINT timeout -t 2 -s KILL python main.py