#!/usr/bin/env python3

from json import load as json_load, dumps as json_dumps

from jsonschema import validate

from simplified_main import test_simplified, SimplifiedCompleteResult, read_test_data_from_json_dict, \
    TestData

# Load json schema
test_data_schema_file_name: str = 'test_data.schema.json'

with open(test_data_schema_file_name, 'r') as test_data_schema_file:
    test_data_schema = json_load(test_data_schema_file)

# Read test config from json file
test_data_file_name: str = 'test_data.json'

with open(test_data_file_name, 'r') as test_data_file:
    complete_test_data = json_load(test_data_file)

# validate test data against json schema (raises exception if not successful...)
validate(complete_test_data, test_data_schema)

simplified_test_data: TestData = read_test_data_from_json_dict(complete_test_data)

test_result: SimplifiedCompleteResult = test_simplified(simplified_test_data)

# write results
result_file_name: str = 'result.json'

with open(result_file_name, 'w') as result_file:
    result_file.write(json_dumps(test_result.to_json_dict(), indent=2))
