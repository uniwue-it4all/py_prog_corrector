FROM beyselein/py_correction_base_image

#ENV PYTHONPATH $WORKDIR:$PYTHONPATH

COPY entrypoint.sh main.py simplified_main.py test_data.schema.json /data/

ENTRYPOINT ["./entrypoint.sh"]