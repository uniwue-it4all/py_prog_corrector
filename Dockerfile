FROM python@sha256:abc2a66d8ce0ddf14b1d51d4c1fe83f21059fa1c4952c02116cb9fd8d5cfd5c4

RUN pip install jsonschema && apk update && apk upgrade && apk add vim

LABEL maintainer="b.eyselein@gmail.com"

ARG WorkDir=/data

ENV PYTHONPATH $WorkDir:$PYTHONPATH

COPY entrypoint.sh test_base.py main.py simplified_main.py extended_main.py \
    simplified_test_data.schema.json extended_test_data.schema.json unified_test_data.schema.json $WorkDir/

WORKDIR $WorkDir

ENTRYPOINT ["./entrypoint.sh"]

CMD []