from typing import TypedDict

from common_helpers import TestResult


class TestConfig(TypedDict):
    id: int
    shouldFail: bool
    description: str


class CompleteTestConfig(TypedDict):
    filename: str
    testFilename: str
    testConfigs: list[TestConfig]


class UnitTestCorrectionResult(TestResult):
    testId: int
    description: str
    shouldFail: bool
