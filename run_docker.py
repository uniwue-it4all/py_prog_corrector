#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from pathlib import Path
from subprocess import run as subprocess_run
from sys import stderr
from typing import Optional


@dataclass()
class MountPoint:
    from_path: Path
    to_path: Path
    read_only: bool = False

    def to_bind(self) -> str:
        mount_options: str = f":ro" if self.read_only else ""

        return f"    -v {self.from_path.absolute()}:{self.to_path}{mount_options}"


def check_file_or_exit(file: Path):
    if not file.exists():
        print(f"File {file} is missing!", file=stderr)
        exit(101)


def check_files_or_exit(files: list[Path]):
    for file in files:
        check_file_or_exit(file)


supported_correction_types: list[str] = ["simplified", "unit_test", "normal"]

# noinspection SpellCheckingInspection
img_tag: str = "py_prog_corrector:latest"

parser = ArgumentParser()

parser.add_argument(
    "-t", "--type", dest="correction_type", choices=supported_correction_types, help="Correction Type", required=True
)
parser.add_argument("-p", "--pretty-print", dest="pretty_print", action="store_true", help="Pretty print result file")
parser.add_argument(
    "-k", "--keep-container", dest="keep_container", action="store_true", help="Keep container after run"
)
parser.add_argument("-b", "--build", "--build-image", dest="build_image", action="store_true", help="Build image")
parser.add_argument("--print-command", action="store_true", help="Print run command")
parser.add_argument("exercise_name", help="Name of the exercise folder")

new_args: Namespace = parser.parse_args()

correction_type: Optional[str] = new_args.correction_type

# remove trailing slash from exercise name
exercise_name = new_args.exercise_name[:-1] if new_args.exercise_name.endswith("/") else new_args.exercise_name

# build docker image...
if new_args.build_image:
    subprocess_run(f"docker build -t {img_tag} .", shell=True, check=True)

mount_base_path = Path("/data")
mount_points: list[MountPoint] = []

# create and clear result file
results_folder = Path.cwd() / "results"

if not results_folder.exists():
    results_folder.mkdir()

result_file_path: Path = results_folder / f"{correction_type}_result_{exercise_name}.json"
result_file_path.open("w").truncate()

exercise_folder = Path.cwd() / exercise_name

if correction_type == "simplified":
    user_solution_file_path = exercise_folder / f"{exercise_name}.py"
    test_main_file_path = exercise_folder / "simplified_test_data" / "simplified_test_main.py"
    test_data_file_path = exercise_folder / "simplified_test_data" / "simplified_test_data.json"

    check_files_or_exit([user_solution_file_path, test_main_file_path, test_data_file_path])

    mount_points = [
        MountPoint(result_file_path, mount_base_path / "result.json"),
        MountPoint(user_solution_file_path, mount_base_path / f"{exercise_name}.py", read_only=True),
        MountPoint(test_main_file_path, mount_base_path / "simplified_test_main.py", read_only=True),
        MountPoint(test_data_file_path, mount_base_path / "test_data.json", read_only=True),
    ]

elif correction_type == "unit_test":
    solution_file_name = f"{exercise_name}.py"
    solution_file_path = exercise_folder / solution_file_name

    test_file_name = f"test_{exercise_name}.py"
    test_file_path = exercise_folder / test_file_name

    test_data_file_path = exercise_folder / "unit_test_data" / "unit_test_test_data.json"

    check_files_or_exit([solution_file_path, test_file_path, test_data_file_path])

    default_mount_points = [
        MountPoint(result_file_path, mount_base_path / "result.json"),
        MountPoint(solution_file_path, mount_base_path / solution_file_name, read_only=True, ),
        MountPoint(test_file_path, mount_base_path / test_file_name),
        MountPoint(test_data_file_path, mount_base_path / "test_data.json", read_only=True),
    ]

    unit_test_solutions_folder = exercise_folder / "unit_test_data"
    unit_test_solutions_mount_points = [
        MountPoint(
            unit_test_solution_file, mount_base_path / exercise_name / unit_test_solution_file.name, read_only=True,
        )
        for unit_test_solution_file in unit_test_solutions_folder.glob(f"{exercise_name}_*.py")
    ]

    mount_points = default_mount_points + unit_test_solutions_mount_points

elif correction_type == "normal":
    exercise_file_mounts = [
        MountPoint(file, mount_base_path / file.name, read_only=True)
        for file in exercise_folder.glob("*")
        if file.is_file()
    ]

    mount_points = [
                       MountPoint(result_file_path.absolute(), mount_base_path / "result.json"),
                       # MountPoint(exercise_folder, mount_base_path / exercise_name, read_only=True),
                   ] + exercise_file_mounts

# run correction
mounts: str = "\n".join(mount.to_bind() for mount in mount_points)
container_options = "" if new_args.keep_container else "--rm"
options: str = "-p" if new_args.pretty_print is not None else ""

docker_run_command = f"docker run -it {container_options}\n{mounts}\n    {img_tag} {correction_type} {options}"

if new_args.print_command:
    print(docker_run_command)

run_process = subprocess_run(docker_run_command.replace("\n", ""), shell=True)

exit(run_process.returncode)
