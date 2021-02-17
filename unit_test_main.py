from json import dumps as json_dumps
from pathlib import Path
from subprocess import CompletedProcess, run as subprocess_run
from sys import stderr, argv
from typing import List

from common_helpers import result_file_path, cwd, load_parse_and_check_test_data
from unit_test_model import CompleteTestConfig, UnitTestCorrectionResult

# parse cli args
indent = 2 if "-p" in argv else None

loaded_json = load_parse_and_check_test_data("unit_test")

complete_test_config: CompleteTestConfig = CompleteTestConfig.parse_from_json(loaded_json)

folder_name: str = complete_test_config.folder_name
test_file_name: str = complete_test_config.test_file_name

# read unit test file content
test_file_path = cwd / f"{test_file_name}.py"

if not test_file_path.exists():
    print(f"File {test_file_path} does not exist!", file=stderr)
    exit(23)

test_file_content = test_file_path.read_text()

results: List[UnitTestCorrectionResult] = []

for test_config in complete_test_config.test_configs:
    file_name = complete_test_config.file_name

    file_to_test_path: Path = cwd / folder_name / f"{file_name}_{test_config.id}.py"

    if not file_to_test_path.exists:
        print(f"File {file_to_test_path} does not exist!", file=stderr)
        break

    test_file_path: Path = cwd / folder_name / f"{test_file_name}_{test_config.id}.py"

    test_file_path.write_text(
        test_file_content.replace(f"from {file_name} import", f"from {str(file_to_test_path.name)[:-3]} import")
    )

    completed_process: CompletedProcess = subprocess_run(
        f"(cd {folder_name} && timeout 2 python -m unittest {test_file_path.name})",
        capture_output=True,
        shell=True,
        text=True,
    )

    # test_file_path.unlink()

    result = UnitTestCorrectionResult(
        test_id=test_config.id,
        description=test_config.description,
        should_fail=test_config.should_fail,
        status=completed_process.returncode,
        stdout=completed_process.stdout[:10_000].split("\n")[:50],
        stderr=completed_process.stderr[:10_000].split("\n")[:50],
    )

    results.append(result)

result_file_path.write_text(
    json_dumps(
        [r.to_json_dict() for r in results],
        indent=indent
    )
)
