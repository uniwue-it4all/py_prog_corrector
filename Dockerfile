FROM ls6uniwue/py_correction_base_image

COPY simplified_entrypoint.sh simplified_model.py simplified_test.py simplified_main.py simplified_test_data.schema.json /data/

ENTRYPOINT ["./simplified_entrypoint.sh"]
