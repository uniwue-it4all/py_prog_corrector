FROM beyselein/py_correction_base_image

ARG WORKDIR=/data

#ENV PYTHONPATH $WORKDIR:$PYTHONPATH

COPY entrypoint.sh main.py simplified_main.py test_data.schema.json $WORKDIR/

WORKDIR $WORKDIR

ENTRYPOINT ./entrypoint.sh