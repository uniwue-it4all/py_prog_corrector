FROM python:3-alpine

LABEL maintainer="b.eyselein@gmail.com"

ARG WORKDIR=/data/

RUN apk update && \
    apk upgrade && \
    apk add bash gcc musl-dev && \
    pip install -U pip jsonschema pylint

WORKDIR ${WORKDIR}

COPY .pylintrc main_entrypoint.sh *.py *.schema.json ${WORKDIR}

ENTRYPOINT ["./main_entrypoint.sh"]
