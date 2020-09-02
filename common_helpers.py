from abc import abstractmethod
from dataclasses import dataclass
from json import load as json_load
from pathlib import Path
from sys import stderr
from typing import Dict, List, Tuple, TypeVar, Generic

from jsonschema import validate as json_validate, ValidationError

cwd: Path = Path.cwd()

test_data_path: Path = cwd / "test_data.json"
result_file_path: Path = cwd / "result.json"


@dataclass()
class FileResult:
    file_name: str
    exists: bool

    def to_json_dict(self) -> Dict:
        return {"file_name": self.file_name, "exists": self.exists}

    @staticmethod
    def for_file(file: Path) -> "FileResult":
        return FileResult(file.name, file.exists())


class SingleResult:
    @abstractmethod
    def to_json_dict(self) -> Dict:
        pass


T = TypeVar("T", bound=SingleResult)


@dataclass()
class CompleteResult(Generic[T]):
    file_results: List[FileResult]
    results: List[T]

    def to_json_dict(self) -> Dict:
        return {
            "fileResults": [fr.to_json_dict() for fr in self.file_results],
            "results": [r.to_json_dict() for r in self.results],
        }


def __schema_path_for_correction_type(correction_type: str) -> Path:
    if correction_type == "simplified":
        return cwd / "simplified_test_data.schema.json"
    else:
        return cwd / "unit_test_test_data.schema.json"


def load_parse_and_check_test_data(correction_type: str) -> Tuple[List[FileResult], Dict]:
    test_data_schema_path: Path = __schema_path_for_correction_type(correction_type)

    file_results: List[FileResult] = [
        FileResult.for_file(test_data_schema_path),
        FileResult.for_file(test_data_path),
        FileResult.for_file(result_file_path),
    ]

    missing_files: List[FileResult] = [fr for fr in file_results if not fr.exists]

    if len(missing_files) > 0:
        print(f"Could not find all required files:", file=stderr)

        for f in missing_files:
            print(f"\t{f}", file=stderr)

        exit(21)

    with test_data_schema_path.open("r") as test_data_schema_file:
        test_data_schema = json_load(test_data_schema_file)

    with test_data_path.open("r") as test_config_file:
        loaded_json: Dict = json_load(test_config_file)

    try:
        json_validate(instance=loaded_json, schema=test_data_schema)
    except ValidationError as e:
        print(e)
        exit(22)

    return file_results, loaded_json
