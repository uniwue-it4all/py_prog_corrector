from typing import TypedDict

from common_helpers import TestResult


class TestConfig(TypedDict):
    id: int
    shouldFail: bool
    description: str


class CompleteTestConfig(TypedDict):
    folderName: str
    filename: str
    testFilename: str
    testConfigs: list[TestConfig]


class UnitTestCorrectionResult(TestResult):
    test_id: int
    description: str
    should_fail: bool
