#!/usr/bin/env python3

import json
import sys
import traceback
from io import StringIO

# noinspection PyUnresolvedReferences
from test_main import test, convert_input

if __name__ == '__main__':
    test_data_file_name = 'testdata.json'
    result_file_name = 'result.json'

    with open(test_data_file_name, 'r') as test_data_file, open(result_file_name, 'w') as result_file:

        complete_test_data = json.loads(test_data_file.read())
        function_name = complete_test_data['functionname']

        results = []

        for test_data in complete_test_data['testdata']:
            test_id = test_data['id']
            input_json = test_data['input']
            awaited_output = test_data['output']

            # Convert input
            converted_input = convert_input(input_json)

            # Redirect stdout to variable test_stdout
            sys.stdout = test_stdout = StringIO()

            # noinspection PyBroadException
            try:
                (gotten_output, correctness) = test(converted_input, awaited_output)
                result_type = 'SUCCESS' if correctness else 'NONE'
            except Exception:
                gotten_output = traceback.print_exc()
                result_type = 'FAILURE'

            test_result = {
                'id': test_id,
                'input': input_json,
                'awaited_output': awaited_output,
                'gotten_output': gotten_output,
                'correct': result_type,
                'stdout': test_stdout.getvalue()
            }

            # Revert stdout to 'normal' stdout
            sys.stdout = sys.__stdout__

            results.append(test_result)

        to_write = json.dumps(results, indent=2)

        result_file.write(to_write)
