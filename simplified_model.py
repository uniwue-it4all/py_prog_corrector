from dataclasses import dataclass
from typing import List, Any, Dict


@dataclass()
class SingleSimplifiedTestData:
    id: int
    input: List[Any]
    output: Any

    @staticmethod
    def read_from_json_dict(json_dict: Dict) -> "SingleSimplifiedTestData":
        return SingleSimplifiedTestData(
            json_dict["id"], json_dict["input"], json_dict["output"]
        )


@dataclass()
class TestData:
    base_data: Any
    single_test_data: List[SingleSimplifiedTestData]

    @staticmethod
    def read_from_json_dict(json_dict: Dict) -> "TestData":
        return TestData(
            base_data=json_dict["baseData"] if "baseData" in json_dict else None,
            single_test_data=[
                SingleSimplifiedTestData.read_from_json_dict(single_td_json)
                for single_td_json in json_dict["testData"]
            ],
        )


@dataclass()
class SimplifiedResult:
    test_id: int
    test_input: Any
    awaited: Any
    gotten: Any
    success: str
    stdout: str

    def to_json_dict(self) -> Dict:
        return self.__dict__
        # return {
        #    'id': self.test_id,
        #    'input': self.test_input,
        #    'awaited': self.awaited,
        #    'gotten': self.gotten,
        #    'success': self.success,
        #    'stdout': self.stdout
        # }


@dataclass()
class CompleteSimplifiedResult:
    results: List[SimplifiedResult]

    def to_json_dict(self) -> Dict:
        return {"results": [r.to_json_dict() for r in self.results]}
