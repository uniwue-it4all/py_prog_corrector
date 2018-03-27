#!/usr/bin/env python3

import json
from io import StringIO
import sys

# noinspection PyUnresolvedReferences
from test_main import test, convert_input

if __name__ == '__main__':
    testdata_file_name = 'testdata.json'
    result_file_name = 'results.json'

    with open(testdata_file_name, 'r') as testdata_file, open(result_file_name, 'w') as result_file:

        complete_testdata = json.loads(testdata_file.read())
        function_name = complete_testdata['functionname']

        results = []

        # FIXME: redirect std out to file like >> results!

        for test_data in complete_testdata['testdata']:
            test_id = test_data['id']
            input_json = test_data['input']
            awaited_output = test_data['output']
            sys.stdout = test_stdout = StringIO()

            try:
                converted_input = convert_input(input_json)
                (gotten_output, correctness) = test(converted_input, awaited_output)
            except Exception:
                gotten_output = "FAILURE!"
                correctness = False

            test_result = {
                'id': test_id,
                'input': input_json,
                'awaited_output': awaited_output,
                'gotten_output': gotten_output,
                'correct': correctness,
                'stdout': test_stdout.getvalue()
            }

            sys.stdout = sys.__stdout__

            results.append(test_result)

        result_file.write(json.dumps(results, indent=2))
