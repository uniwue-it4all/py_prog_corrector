# noinspection PyUnresolvedReferences
from solution import ggt


def convert_input(input_json):
    return input_json['a'], input_json['b']


def test(numbers, awaited_output):
    gotten_output = ggt(numbers[0], numbers[1])

    return gotten_output, gotten_output == awaited_output
