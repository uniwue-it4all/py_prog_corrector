#!/usr/bin/env python3

import sys
from importlib import import_module
from io import StringIO
from json import loads as json_loads, dumps as json_dumps
from typing import List, Tuple
from unittest import TestCase, TextTestRunner, TestResult, TestSuite

testdata_file_name: str = 'testdata.json'
result_file_name: str = 'result.json'

# Read test config from json file
with open(testdata_file_name, 'r') as testdata_file:
    testdata = json_loads(testdata_file.read())

problem_file_name: str = testdata['class_ut'].lower()

# FIXME: capture syntax error...?

# Import learner solution, get test class from import
imported_module = import_module(problem_file_name)
class_under_test = getattr(imported_module, 'CircleTest')

test_results = []

# FIXME: run tests in dependent order...

for func_to_test in testdata['methods']:
    test_func_name: str = "test_{}".format(func_to_test['name'])

    suite = TestSuite()
    suite.addTest(class_under_test(test_func_name))

    # Redirect stdout to variable test_stdout
    sys.stdout = test_stdout = StringIO()

    test_output_target: StringIO = StringIO()

    runner: TextTestRunner = TextTestRunner(stream=test_output_target)
    test_result: TestResult = runner.run(suite)

    # Reset stdout to original
    sys.stdout = sys.__stdout__

    error_msgs: List[List[str]] = []

    errors_and_failures: List[Tuple[TestCase, str]] = test_result.errors + test_result.failures
    for error in errors_and_failures:
        error_msgs.append(error[1].split('\n'))

    test_results.append({
        'name': test_func_name,
        'successful': len(errors_and_failures) == 0,
        'errors': error_msgs,
        'sysout': test_stdout.getvalue(),
    })

with open(result_file_name, 'w') as result_file:
    result_file.write(json_dumps(test_results, indent=2))
