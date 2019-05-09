from typing import List

from solution import longest_string


def convert_base_data(json_base_data):
    return None


def convert_test_input(base_data, input_json: List[str]) -> List[str]:
    return input_json


def test(base_data, my_list: List[str], awaited_output: str):
    gotten_output = longest_string(my_list)
    return gotten_output, gotten_output == awaited_output
