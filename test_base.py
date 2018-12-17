from typing import Dict, TypeVar, Generic, List, Any
from abc import ABC, abstractmethod

TR = TypeVar('TR')


class CompleteTestResult(ABC, Generic[TR]):
    def __init__(self, results: List[TR]):
        self.results: List[TR] = results

    @abstractmethod
    def to_json_dict(self) -> Dict[str, Any]:
        pass


class SingleTestResult(ABC):
    @abstractmethod
    def to_json_dict(self) -> Dict:
        pass
