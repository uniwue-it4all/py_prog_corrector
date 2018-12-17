#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from json import loads as json_loads, dumps as json_dumps

# noinspection Mypy
from jsonschema import validate, ValidationError

from test_base import CompleteTestResult


def parse_args() -> Namespace:
    # Configure program arguments
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument('--extended', action='store_true')
    parser.add_argument('--test-data-file')
    parser.add_argument('--solution-file')
    parser.add_argument('--result-file')

    return parser.parse_args()


args: Namespace = parse_args()

print(args)

is_extended: bool = args.extended

test_data_file_name: str = 'test_data.json' if args.test_data_file is None else args.test_data_file

test_data_schema_file_name: str = "{}_test_data.schema.json".format('extended' if is_extended else 'simplified')

result_file_name: str = 'result.json' if args.result_file is None else args.result_file

if is_extended:
    from extended_main import test_extended
else:
    from simplified_main import test_simplified

# Load json schema
with open(test_data_schema_file_name, 'r') as test_data_schema_file:
    test_data_schema = json_loads(test_data_schema_file.read())

# Read test config from json file
with open(test_data_file_name, 'r') as test_data_file:
    test_data = json_loads(test_data_file.read())

# Try to validate test data
try:
    validate(test_data, test_data_schema)
except ValidationError:
    exit(2)

test_result: CompleteTestResult
if is_extended:
    test_result = test_extended(test_data)
else:
    test_result = test_simplified(test_data)

# write results
with open(result_file_name, 'w') as result_file:
    result_file.write(json_dumps(test_result.to_json_dict(), indent=2))
