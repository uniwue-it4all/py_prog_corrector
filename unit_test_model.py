from dataclasses import dataclass
from typing import List, Dict

from common_helpers import SingleResult


@dataclass()
class TestConfig:
    id: int
    should_fail: bool
    description: str

    @staticmethod
    def parse_from_json(json_object: Dict) -> "TestConfig":
        return TestConfig(
            id=json_object["id"], should_fail=json_object["shouldFail"], description=json_object["description"]
        )


@dataclass()
class CompleteTestConfig:
    folder_name: str
    file_name: str
    test_file_name: str
    test_configs: List[TestConfig]

    @staticmethod
    def parse_from_json(json_object: Dict) -> "CompleteTestConfig":
        return CompleteTestConfig(
            folder_name=json_object["folderName"],
            file_name=json_object["filename"],
            test_file_name=json_object["testFilename"],
            test_configs=[TestConfig.parse_from_json(sub_object) for sub_object in json_object["testConfigs"]],
        )


@dataclass()
class UnitTestCorrectionResult(SingleResult):
    test_id: int
    description: str
    should_fail: bool
    status: int
    stdout: str
    stderr: str

    def to_json_dict(self) -> Dict:
        test_failed = self.status != 0

        return {
            "testId": self.test_id,
            "description": self.description,
            "testFailed": test_failed,
            "successful": test_failed == self.should_fail,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }
