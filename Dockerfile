#FROM python@sha256:5a2deb631d2526a3a6b7226917ee32dc419b95dc1c12267d4562a8c8744a7388
FROM python:3-alpine

RUN pip install jsonschema && apk update && apk upgrade && apk add vim

LABEL maintainer="b.eyselein@gmail.com"

ARG WorkDir=/data

ENV PYTHONPATH $WorkDir:$PYTHONPATH

COPY entrypoint.sh test_base.py main.py simplified_main.py extended_main.py simplified_test_data.schema.json extended_test_data.schema.json $WorkDir/

WORKDIR $WorkDir

ENTRYPOINT ["./entrypoint.sh"]

CMD []