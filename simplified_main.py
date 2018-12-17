#!/usr/bin/env python3

import sys
from io import StringIO
from json import loads as json_loads, dumps as json_dumps
from traceback import format_exc as traceback_format_exc
from typing import List, Any

# noinspection PyUnresolvedReferences
from test_main import test, convert_base_data, convert_test_input

test_data_file_name: str = 'testdata.json'
result_file_name: str = 'result.json'


class SingleResult:
    def __init__(self, test_id: int, test_input: Any, awaited: Any, gotten: Any, success: str, stdout: str):
        self.test_id: int = test_id
        self.test_input: Any = test_input
        self.awaited: Any = awaited
        self.gotten: Any = gotten
        self.success: str = success
        self.stdout: str = stdout


def perform_test(base_data: Any, test_data: Any) -> SingleResult:
    test_id: int = test_data['id']
    test_input: Any = test_data['input']
    awaited_output: Any = test_data['output']

    # Convert input
    converted_input: Any = convert_test_input(base_data, test_input)

    # Redirect stdout to variable test_stdout
    sys.stdout = test_stdout = StringIO()

    # noinspection PyBroadException
    try:
        gotten_output, correctness = test(base_data, converted_input, awaited_output)
        success = 'COMPLETE' if correctness else 'NONE'
    except:
        gotten_output = traceback_format_exc()
        success = 'ERROR'

    # Revert stdout to 'normal' stdout
    sys.stdout = sys.__stdout__

    return SingleResult(test_id, test_input, awaited_output, gotten_output, success, test_stdout.getvalue())


def main_test(complete_test_data: Any) -> List[SingleResult]:
    base_data = None
    if 'baseData' in complete_test_data:
        base_data = convert_base_data(complete_test_data['baseData'])

    test_results: List[SingleResult] = []

    for test_data in complete_test_data['testdata']:
        single_result: SingleResult = perform_test(base_data, test_data)
        test_results.append(single_result)

    return test_results


with open(test_data_file_name, 'r') as test_data_file:
    complete_test_data = json_loads(test_data_file.read())

results: List[SingleResult]
try:
    results = main_test(complete_test_data)
    result_type = 'run_through'
    errors = ''
except SyntaxError:
    results = []
    result_type = 'syntax_error'
    errors = traceback_format_exc()

to_write = json_dumps({
    'result_type': result_type,
    'results': list(map(lambda o: o.__dict__, results)),
    'errors': errors
})  # , indent=2)

with open('result.json', 'w') as result_file:
    result_file.write(to_write)
