from json import load as json_load
from pathlib import Path
from sys import stderr

from jsonschema import validate as json_validate, ValidationError

cwd: Path = Path.cwd()

test_data_path: Path = cwd / "test_data.json"
result_file_path: Path = cwd / "result.json"


def __schema_path_for_correction_type__(correction_type: str) -> Path:
    if correction_type == "simplified":
        return cwd / "simplified_test_data.schema.json"
    else:
        return cwd / "unit_test_test_data.schema.json"


def load_parse_and_check_test_data(correction_type: str) -> dict:
    test_data_schema_path: Path = __schema_path_for_correction_type__(correction_type)

    files_to_check: list[Path] = [test_data_schema_path, test_data_path, result_file_path]

    missing_files: list[Path] = [fr for fr in files_to_check if not fr.exists()]

    if len(missing_files) > 0:
        print(f"Could not find all required files:", file=stderr)

        for f in missing_files:
            print(f"\t{f}", file=stderr)

        exit(21)

    with test_data_schema_path.open("r") as test_data_schema_file:
        test_data_schema = json_load(test_data_schema_file)

    with test_data_path.open("r") as test_config_file:
        loaded_json: dict = json_load(test_config_file)

    try:
        json_validate(instance=loaded_json, schema=test_data_schema)
    except ValidationError as e:
        print(e)
        exit(22)

    return loaded_json
