# noinspection PyUnresolvedReferences
from solution import average


def convert_input(input_json):
    return input_json


def test(my_list, awaited_output):
    gotten_output = average(my_list)

    return gotten_output, gotten_output == awaited_output
