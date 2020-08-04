FROM ls6uniwue/py_correction_base_image

COPY entrypoint.sh simplified_model.py simplified_main.py main.py simplified_test_data.schema.json /data/

ENTRYPOINT ["./entrypoint.sh"]
