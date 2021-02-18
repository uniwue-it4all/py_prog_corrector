from dataclasses import dataclass


@dataclass()
class TestConfig:
    id: int
    should_fail: bool
    description: str

    @staticmethod
    def parse_from_json(json_object: dict) -> "TestConfig":
        return TestConfig(
            id=json_object["id"], should_fail=json_object["shouldFail"], description=json_object["description"]
        )


@dataclass()
class CompleteTestConfig:
    folder_name: str
    file_name: str
    test_file_name: str
    test_configs: list[TestConfig]

    @staticmethod
    def parse_from_json(json_object: dict) -> "CompleteTestConfig":
        return CompleteTestConfig(
            folder_name=json_object["folderName"],
            file_name=json_object["filename"],
            test_file_name=json_object["testFilename"],
            test_configs=[TestConfig.parse_from_json(sub_object) for sub_object in json_object["testConfigs"]],
        )


@dataclass()
class UnitTestCorrectionResult:
    test_id: int
    description: str
    should_fail: bool
    status: int
    stdout: str
    stderr: str

    def to_json_dict(self) -> dict:
        test_failed = self.status != 0

        return {
            "testId": self.test_id,
            "description": self.description,
            "successful": test_failed == self.should_fail,
            "shouldFail": self.should_fail,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }
