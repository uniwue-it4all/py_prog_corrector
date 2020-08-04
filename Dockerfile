FROM ls6uniwue/py_correction_base_image

COPY *entrypoint.sh *.py *.schema.json /data/

ENTRYPOINT ["./main_entrypoint.sh"]
