#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
from subprocess import run as subprocess_run
from sys import argv, stderr
from typing import List, Optional


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


def check_files_or_exit(files: List[Path]):
    for file in files:
        check_file_or_exit(file)


supported_correction_types: List[str] = ["simplified", "unit_test", "normal"]

# noinspection SpellCheckingInspection
img_tag: str = "py_prog_corrector:latest"

args: List[str] = argv[1:]
positional_args: List[str] = []

correction_type: Optional[str] = None
build_image: bool = False
keep_container: bool = False
print_run_command: bool = False
pretty_print: Optional[str] = None

i: int = 0
while i < len(args):
    if args[i] in ["-t", "--type"]:
        correction_type_value = args[i + 1]

        if correction_type_value in supported_correction_types:
            correction_type = correction_type_value
        else:
            print(f"Correction type {correction_type_value} is not supported!")
            exit(2)

        i += 1
    elif args[i] in ["-p"]:
        pretty_print = args[i]
    elif args[i] in ["-k", "--keep-container"]:
        keep_container = True
    elif args[i] in ["-b", "--build", "--build-image"]:
        build_image = True
    elif args[i] in ["--print-command"]:
        print_run_command = True
    else:
        positional_args.append(args[i])

    i += 1

if correction_type is None or len(positional_args) == 0:
    print("No correction type or exercise name was set!", file=stderr)
    exit(1)

exercise_name: str = positional_args[0]

# remove trailing slash from exercise name
exercise_name = exercise_name[:-1] if exercise_name.endswith("/") else exercise_name

# build docker image...
if build_image:
    subprocess_run(f"docker build -t {img_tag} .", shell=True, check=True)

mount_base_path = Path("/data")
mount_points: List[MountPoint] = []

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
        MountPoint(solution_file_path, mount_base_path / exercise_name / solution_file_name, read_only=True,),
        MountPoint(test_file_path, mount_base_path / exercise_name / test_file_name),
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
container_options = "" if keep_container else "--rm"
options: str = pretty_print if pretty_print is not None else ""

docker_run_command = f"docker run -it {container_options}\n{mounts}\n    {img_tag} {correction_type} {options}"

if print_run_command:
    print(docker_run_command)

run_process = subprocess_run(docker_run_command.replace("\n", ""), shell=True)

exit(run_process.returncode)
