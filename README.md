# Python Test Image for it4all

## Exit codes

* `2`: Validation error test data vs. test data schema

## `test_main.py` base

```python
from typing import Any

# noinspection PyUnresolvedReferences
from solution import ...


def convert_base_data(json_base_data):
    """
    Unused
    """
    pass


def convert_test_input(base_data, input_json):
    """
    Converts input_json to test ready values
    """
    pass


def test(base_data, test_input, awaited_output) -> (Any, bool):
    """
    Runs test. Returns test result and correctness of test result
    """
    pass
```