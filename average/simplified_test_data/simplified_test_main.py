from typing import Any, Tuple, Optional, List

from average import average

epsilon = 1e-3


def convert_base_data(json_base_data: Any) -> Any:
    return None


def convert_test_input(base_data: Any, input_json: List[int]) -> List[int]:
    return input_json


def test(
    base_data: Any, my_list: List[int], awaited_output: Optional[float]
) -> Tuple[Any, bool]:
    gotten_output: Any = average(my_list)

    if awaited_output is None:
        correctness: bool = gotten_output is None
    elif isinstance(awaited_output, str) or isinstance(gotten_output, str):
        correctness = gotten_output == awaited_output
    else:
        correctness = abs(gotten_output - awaited_output) < epsilon

    return gotten_output, correctness
