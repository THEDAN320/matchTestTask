from typing import List
import os


if os.name == "nt":
    sep = "\\"
else:
    sep = "/"

files_path = f"{os.getcwd()}{sep}files"


def get_files_list() -> List[str]:
    return os.listdir(files_path)


def get_file_path(file) -> str:
    return f"{files_path}{sep}{file}"
