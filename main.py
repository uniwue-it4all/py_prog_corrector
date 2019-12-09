#!/usr/bin/env python3
from json import load as json_load, dumps as json_dumps
from typing import List

# noinspection Mypy
from jsonschema import validate

from simplified_main import test_simplified, read_test_data_from_json_dict, TestData, SimplifiedResult

# read json schema and test config from json files
with open('test_data.schema.json', 'r') as test_data_schema_file:
    test_data_schema = json_load(test_data_schema_file)

with open('test_data.json', 'r') as test_data_file:
    complete_test_data = json_load(test_data_file)

# validate test data against json schema (raises exception if not successful...)
validate(complete_test_data, test_data_schema)

simplified_test_data: TestData = read_test_data_from_json_dict(complete_test_data)

test_result: List[SimplifiedResult] = test_simplified(simplified_test_data)

# write results
with open('result.json', 'w') as result_file:
    result_file.write(json_dumps([t.to_json_dict() for t in test_result]))
