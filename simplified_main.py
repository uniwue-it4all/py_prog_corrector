import sys
from dataclasses import dataclass
from io import StringIO
from traceback import format_exc as traceback_format_exc
from typing import List, Any, Dict

# noinspection PyUnresolvedReferences,Mypy
from test_main import test, convert_base_data, convert_test_input


@dataclass()
class SingleSimplifiedTestData:
    id: int
    input: List[Any]
    output: Any


@dataclass()
class TestData:
    base_data: Any
    single_test_data: List[SingleSimplifiedTestData]


@dataclass()
class SimplifiedResult:
    test_id: int
    test_input: Any
    awaited: Any
    gotten: Any
    success: str
    stdout: str

    def to_json_dict(self) -> Dict:
        return {
            'id': self.test_id,
            'input': self.test_input,
            'awaited': self.awaited,
            'gotten': self.gotten,
            'success': self.success,
            'stdout': self.stdout
        }


def read_test_data_from_json_dict(json_dict: Dict) -> TestData:
    single_test_data: List[SingleSimplifiedTestData] = [
        SingleSimplifiedTestData(
            int(single_td_json['id']),
            single_td_json['input'],
            single_td_json['output']
        ) for single_td_json in json_dict['testData']
    ]

    return TestData(
        json_dict['baseData'] if 'baseData' in json_dict else None,
        single_test_data
    )


def __perform_test__(base_data: Any, test_data: SingleSimplifiedTestData) -> SimplifiedResult:
    test_input: Any = test_data.input
    awaited_output: Any = test_data.output

    # Convert input
    converted_input: Any = convert_test_input(base_data, test_input)

    # Redirect stdout to variable test_stdout
    sys.stdout = test_stdout = StringIO()

    # noinspection PyBroadException
    try:
        gotten_output, correctness = test(base_data, converted_input, awaited_output)
        success = 'COMPLETE' if correctness else 'NONE'
    except Exception:
        gotten_output = traceback_format_exc()
        success = 'ERROR'

    # Revert stdout to 'normal' stdout
    sys.stdout = sys.__stdout__

    return SimplifiedResult(test_data.id, test_input, awaited_output, gotten_output, success, test_stdout.getvalue())


def test_simplified(complete_test_data: TestData) -> List[SimplifiedResult]:
    base_data = None
    if complete_test_data.base_data is not None:
        base_data = convert_base_data(complete_test_data.base_data)

    test_results: List[SimplifiedResult] = []

    for test_data in complete_test_data.single_test_data:
        single_result: SimplifiedResult = __perform_test__(base_data, test_data)
        test_results.append(single_result)

    return test_results
