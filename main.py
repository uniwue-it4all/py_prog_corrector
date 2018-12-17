#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from json import loads as json_loads, dumps as json_dumps

# noinspection Mypy
from jsonschema import validate

from test_base import CompleteTestResult

test_data_file_name: str = 'test_data.json'
test_data_schema_file_name: str = 'unified_test_data.schema.json'


def parse_args() -> Namespace:
    # Configure program arguments
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument('--extended', action='store_true')
    parser.add_argument('--test-data-file')
    parser.add_argument('--solution-file')
    parser.add_argument('--result-file')

    return parser.parse_args()


args: Namespace = parse_args()

is_extended: bool = args.extended

result_file_name: str = 'result.json' if args.result_file is None else args.result_file

if is_extended:
    from extended_main import test_extended, read_extended_test_data_from_json_dict, ExtendedTestData
else:
    from simplified_main import test_simplified, read_simplified_test_data_from_json_dict, SimplifiedTestData

# Load json schema
with open(test_data_schema_file_name, 'r') as test_data_schema_file:
    test_data_schema = json_loads(test_data_schema_file.read())

# Read test config from json file
with open(test_data_file_name, 'r') as test_data_file:
    complete_test_data = json_loads(test_data_file.read())

# validate test data against json schema (raises exception if not successful...)
validate(complete_test_data, test_data_schema)

test_result: CompleteTestResult
if is_extended:
    extended_test_data: ExtendedTestData = read_extended_test_data_from_json_dict(complete_test_data['extended'])
    test_result = test_extended(extended_test_data)
else:
    simplified_test_data: SimplifiedTestData = read_simplified_test_data_from_json_dict(
        complete_test_data['simplified'])
    test_result = test_simplified(simplified_test_data)

# write results
with open(result_file_name, 'w') as result_file:
    result_file.write(json_dumps(test_result.to_json_dict(), indent=2))
