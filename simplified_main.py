import sys
from io import StringIO
from json import dumps as json_dumps
from traceback import format_exc as traceback_format_exc
from typing import Any, List

from common_helpers import (
    simplified_test_data_schema_path,
    result_file_path,
    load_parse_and_check_test_data,
    CompleteResult,
)
from simplified_model import SimplifiedResult, SingleSimplifiedTestData, TestData
from simplified_test_main import convert_base_data, test, convert_test_input


def __perform_test__(base_data: Any, test_data: SingleSimplifiedTestData) -> SimplifiedResult:
    # Convert input
    converted_input: Any = convert_test_input(base_data, test_data.input)

    # Redirect stdout to variable test_stdout
    sys.stdout = test_stdout = StringIO()

    # noinspection PyBroadException
    try:
        gotten_output, correctness = test(base_data, converted_input, test_data.output)
        success = "COMPLETE" if correctness else "NONE"
    except Exception:
        gotten_output = traceback_format_exc()
        success = "ERROR"

    # Revert stdout to 'normal' stdout
    sys.stdout = sys.__stdout__

    return SimplifiedResult(
        test_data.id, test_data.input, test_data.output, gotten_output, success, test_stdout.getvalue()
    )


# parse cli args
indent = 2 if "-p" in sys.argv else None

# load and parse test data
file_results, loaded_json = load_parse_and_check_test_data(simplified_test_data_schema_path)

simplified_test_data: TestData = TestData.read_from_json_dict(loaded_json)

converted_base_data = (
    None if simplified_test_data.base_data is None else convert_base_data(simplified_test_data.base_data)
)

# execute tests
simplified_results: List[SimplifiedResult] = [
    __perform_test__(converted_base_data, test_data) for test_data in simplified_test_data.single_test_data
]

# write results
result_file_path.write_text(
    json_dumps(
        CompleteResult(file_results, simplified_results).to_json_dict(), indent=indent
    )
)
