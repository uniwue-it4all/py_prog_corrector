#!/usr/bin/env python3

import json
import sys
import traceback
from io import StringIO
from typing import Dict, List, Any


class SingleResult:
    def __init__(self, test_id: int, test_input: Dict, awaited: Any, gotten: Any, success: str, stdout: str):
        self.test_id = test_id
        self.test_input = test_input
        self.awaited = awaited
        self.gotten = gotten
        self.success = success
        self.stdout = stdout


def main_test(test_data_file_content: str) -> List[SingleResult]:
    complete_test_data = json.loads(test_data_file_content)

    base_data = None
    if 'baseData' in complete_test_data:
        base_data = convert_base_data(complete_test_data['baseData'])

    test_results: List[SingleResult] = []

    for test_data in complete_test_data['testdata']:
        test_id = test_data['id']
        test_input = test_data['input']
        awaited_output = test_data['output']

        # Convert input
        converted_input = convert_test_input(base_data, test_input)

        # Redirect stdout to variable test_stdout
        sys.stdout = test_stdout = StringIO()

        # noinspection PyBroadException
        try:
            (gotten_output, correctness) = test(base_data, converted_input, awaited_output)
            success = 'COMPLETE' if correctness else 'NONE'
        except:
            gotten_output = traceback.format_exc()
            success = 'ERROR'

        test_result = SingleResult(test_id, test_input, awaited_output, gotten_output, success, test_stdout.getvalue())

        # Revert stdout to 'normal' stdout
        sys.stdout = sys.__stdout__

        test_results.append(test_result)

    return test_results


if __name__ == '__main__':

    with open('testdata.json', 'r') as test_data_file, open('result.json', 'w') as result_file:
        try:
            # noinspection PyUnresolvedReferences
            from test_main import test, convert_base_data, convert_test_input

            results = main_test(test_data_file.read())
            result_type = 'run_through'
            errors = ''

        except SyntaxError:
            results = []
            result_type = 'syntax_error'
            errors = traceback.format_exc()

        to_write = json.dumps({
            'result_type': result_type,
            'results': list(map(lambda o: o.__dict__, results)),
            'errors': errors
        }, indent=2)

        result_file.write(to_write)
