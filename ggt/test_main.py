# noinspection PyUnresolvedReferences
from solution import ggt


def convert_input(input_json):
    return input_json


def test(numbers, awaited_output):
    a, b = numbers[0], numbers[1]

    gotten_output = ggt(a, b)

    return gotten_output, gotten_output == awaited_output
