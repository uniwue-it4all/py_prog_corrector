from json import dumps as json_dumps
from pathlib import Path
from subprocess import CompletedProcess, run as subprocess_run
from sys import stderr, argv
from typing import List, Optional

from common_helpers import result_file_path, cwd, load_parse_and_check_test_data
from unit_test_model import CompleteTestConfig, UnitTestCorrectionResult, TestConfig

# parse cli args
indent: Optional[int] = 2 if "-p" in argv else None

# consts
folder_name: str = 'app_under_test'

complete_test_config: CompleteTestConfig = load_parse_and_check_test_data()

file_name: str = complete_test_config['filename']
test_file_name: str = complete_test_config['testFilename']

# read unit test file content
main_test_file_path: Path = cwd / f"{test_file_name}.py"

if not main_test_file_path.exists():
    print(f"File {main_test_file_path} does not exist!", file=stderr)
    exit(23)

test_file_content: str = main_test_file_path.read_text()


def perform_test(test_config: TestConfig) -> Optional[UnitTestCorrectionResult]:
    test_id: int = test_config['id']

    file_to_test_path: Path = cwd / folder_name / f"{file_name}_{test_id}.py"

    if not file_to_test_path.exists:
        print(f"File {file_to_test_path} does not exist!", file=stderr)
        return None

    test_file_path: Path = cwd / folder_name / f"{test_file_name}_{test_id}.py"

    test_file_path.write_text(
        test_file_content.replace(f"from {file_name} import", f"from {str(file_to_test_path.name)[:-3]} import")
    )

    completed_process: CompletedProcess = subprocess_run(
        f"(cd {folder_name} && timeout 2 python -m unittest {test_file_path.name})",
        capture_output=True,
        shell=True,
        text=True,
    )

    return UnitTestCorrectionResult(
        testId=test_id,
        description=test_config['description'],
        shouldFail=test_config['shouldFail'],
        testSuccessful=completed_process.returncode == 0,
        stdout=completed_process.stdout[:10_000].split("\n")[:50],
        stderr=completed_process.stderr[:10_000].split("\n")[:50],
    )


results: List[UnitTestCorrectionResult] = [
    perform_test(test_config) for test_config in complete_test_config['testConfigs']
]

result_file_path.write_text(
    json_dumps(results, indent=indent)
)
