from dataclasses import dataclass
from json import dumps as json_dumps
from subprocess import run as subprocess_run, CompletedProcess
from sys import argv

from common_helpers import result_file_path

indent = 2 if "-p" in argv else None


@dataclass()
class NormalCorrectionResult:
    successful: bool
    stdout: str
    stderr: str

    def to_json_dict(self) -> dict[str, any]:
        return self.__dict__


completed_process: CompletedProcess = subprocess_run(
    "python -m unittest discover",
    capture_output=True,
    shell=True,
    text=True
)

result = NormalCorrectionResult(
    successful=completed_process.returncode == 0,
    stdout=completed_process.stdout[:10_000].split("\n")[:50],
    stderr=completed_process.stderr[:10_000].split("\n")[:50]
)

result_file_path.write_text(json_dumps(result.to_json_dict(), indent=indent))
