FROM python:3-alpine

RUN pip install --upgrade pip jsonschema

LABEL maintainer="b.eyselein@gmail.com"

ARG WorkDir=/data

ENV PYTHONPATH $WorkDir:$PYTHONPATH

COPY entrypoint.sh test_base.py main.py simplified_main.py extended_main.py unified_test_data.schema.json $WorkDir/

WORKDIR $WorkDir

ENTRYPOINT ["./entrypoint.sh"]

CMD []