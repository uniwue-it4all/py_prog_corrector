import sys
from importlib import import_module
from io import StringIO
from typing import Dict, Any
from typing import List, Tuple
from unittest import TestCase, TextTestRunner, TestResult, TestSuite

from test_base import SingleTestResult, CompleteTestResult


class ExtendedTestData:
    def __init__(self, module_name: str, class_under_test_name: str, methods: List[Any]):
        self.module_name: str = module_name
        self.class_under_test_name: str = class_under_test_name
        self.methods: List[Any] = methods


class ExtendedResult(SingleTestResult):
    def __init__(self, test_func_name: str, successful: bool, errors: List[List[str]], sys_out: str):
        self.test_func_name: str = test_func_name
        self.successful: bool = successful
        self.errors: List[List[str]] = errors
        self.sys_out: str = sys_out

    def to_json_dict(self) -> Dict[str, Any]:
        return {
            'name': self.test_func_name,
            'successful': self.successful,
            'errors': self.errors,
            'sysout': self.sys_out,
        }


class ExtendedCompleteTestResult(CompleteTestResult[ExtendedResult]):
    def __init__(self, results: List[ExtendedResult]):
        super().__init__(results)

    def to_json_dict(self) -> Dict[str, Any]:
        return {
            "results": list(map(lambda r: r.to_json_dict(), self.results))
        }


def read_extended_test_data_from_json_dict(json_dict: Dict) -> ExtendedTestData:
    return ExtendedTestData(
        json_dict['module_name'],
        json_dict['class_ut'],
        json_dict['methods']
    )


def test_extended(test_data: ExtendedTestData) -> ExtendedCompleteTestResult:
    module_name: str = 'extended_tests'  # test_data.module_name
    class_under_test_name: str = test_data.class_under_test_name

    # FIXME: capture syntax error...?

    # Import learner solution, get test class from import
    imported_module = import_module(module_name)
    class_under_test = getattr(imported_module, "{}Test".format(class_under_test_name))

    test_results: List[ExtendedResult] = []
    for func_to_test in test_data.methods:
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

        test_results.append(
            ExtendedResult(test_func_name, len(errors_and_failures) == 0, error_msgs, test_stdout.getvalue()))

    return ExtendedCompleteTestResult(test_results)
