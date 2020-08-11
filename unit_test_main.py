from json import dumps as json_dumps
from sys import stderr, argv
from typing import Optional, List

from common_helpers import (
    result_file_path,
    cwd,
    unit_test_test_data_schema_path,
    load_parse_and_check_test_data,
    CompleteResult,
    FileResult,
)
from unit_test_model import CompleteTestConfig, UnitTestCorrectionResult
from unit_test_test_runner import run_test

# parse cli args
indent = 2 if "-p" in argv else None

file_results, loaded_json = load_parse_and_check_test_data(unit_test_test_data_schema_path)

complete_test_config: CompleteTestConfig = CompleteTestConfig.parse_from_json(loaded_json)

folder_name: str = complete_test_config.folder_name
test_file_name: str = complete_test_config.test_file_name

# read unit test file content
test_file_path = cwd / folder_name / f"{test_file_name}.py"
file_results.append(FileResult.for_file(test_file_path))

test_file_content: Optional[str] = test_file_path.read_text()
if not test_file_path.exists():
    exit(23)

if test_file_content is None:
    print(f"There is no test file {test_file_path}!", file=stderr)
    exit(24)

results: List[UnitTestCorrectionResult] = []

for test_config in complete_test_config.test_configs:
    file_result, result = run_test(
        cwd, test_config, test_file_content, folder_name, complete_test_config.file_name, test_file_name,
    )

    file_results.append(file_result)

    if isinstance(result, UnitTestCorrectionResult):
        results.append(result)

complete_result: CompleteResult[UnitTestCorrectionResult] = CompleteResult(file_results, results)

result_file_path.write_text(json_dumps(complete_result.to_json_dict(), indent=indent))
