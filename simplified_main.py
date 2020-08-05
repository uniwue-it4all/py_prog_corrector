#!/usr/bin/env python3
from json import load as json_load, dumps as json_dumps
from sys import argv
from typing import List

from jsonschema import validate, ValidationError

from simplified_model import CompleteSimplifiedResult
from simplified_test import test_simplified, TestData

# parse cli args
args: List[str] = argv
if '-p' in args:
    indent = 2
else:
    indent = None

# read json schema and test config from json files
with open('simplified_test_data.schema.json', 'r') as test_data_schema_file:
    test_data_schema = json_load(test_data_schema_file)

with open('test_data.json', 'r') as test_data_file:
    complete_test_data = json_load(test_data_file)

# validate test data against json schema (raises exception if not successful...)
try:
    validate(complete_test_data, test_data_schema)
except ValidationError as e:
    print(e)

simplified_test_data: TestData = TestData.read_from_json_dict(complete_test_data)

test_result: CompleteSimplifiedResult = test_simplified(simplified_test_data)

# write results
with open('result.json', 'w') as result_file:
    result_file.write(
        json_dumps(test_result.to_json_dict(), indent=indent)
    )
