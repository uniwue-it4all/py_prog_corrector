from dataclasses import dataclass

from common_helpers import SingleResult


@dataclass()
class SingleSimplifiedTestData:
    id: int
    input: list[any]
    output: any

    @staticmethod
    def read_from_json_dict(json_dict: dict) -> "SingleSimplifiedTestData":
        return SingleSimplifiedTestData(json_dict["id"], json_dict["input"], json_dict["output"])


@dataclass()
class TestData:
    base_data: any
    single_test_data: list[SingleSimplifiedTestData]

    @staticmethod
    def read_from_json_dict(json_dict: dict) -> "TestData":
        return TestData(
            base_data=json_dict["baseData"] if "baseData" in json_dict else None,
            single_test_data=[
                SingleSimplifiedTestData.read_from_json_dict(single_td_json) for single_td_json in json_dict["testData"]
            ],
        )


@dataclass()
class SimplifiedResult(SingleResult):
    test_id: int
    test_input: any
    awaited: any
    gotten: any
    success: str
    stdout: str

    def to_json_dict(self) -> dict[str, any]:
        return {
            "testId": self.test_id,
            "testInput": self.test_input,
            "awaited": self.awaited,
            "gotten": self.gotten,
            "success": self.success,
            "stdout": self.stdout,
        }
