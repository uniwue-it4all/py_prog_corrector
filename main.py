#!/usr/bin/env python3

import json
from converter import *

from solution import *

if __name__ == "__main__":
    with open('testdata.json', 'r') as testdata_file:
        complete_testdata = json.loads(testdata_file.read())

        for testdata in complete_testdata:
            input = testdata['input']
            output = testdata['output']

            converted_input = convert_input(input)

            assert avgAlterPatienten(converted_input) == output
