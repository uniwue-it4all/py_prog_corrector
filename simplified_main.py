import sys
from io import StringIO
from json import dumps as json_dumps
from traceback import format_exc as traceback_format_exc

from common_helpers import result_file_path, load_parse_and_check_test_data
from simplified_model import SimplifiedResult, SingleSimplifiedTestData, TestData
from simplified_test_main import convert_base_data, test, convert_test_input


def __perform_test__(base_data: any, test_data: SingleSimplifiedTestData) -> SimplifiedResult:
    # Convert input
    converted_input: any = convert_test_input(base_data, test_data.input)

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
loaded_json = load_parse_and_check_test_data("simplified")

simplified_test_data: TestData = TestData.read_from_json_dict(loaded_json)

converted_base_data = (
    None if simplified_test_data.base_data is None else convert_base_data(simplified_test_data.base_data)
)

# execute tests
simplified_results: list[SimplifiedResult] = [
    __perform_test__(converted_base_data, test_data) for test_data in simplified_test_data.single_test_data
]

# write results
result_file_path.write_text(
    json_dumps(
        [sr.to_json_dict() for sr in simplified_results],
        indent=indent
    )
)
