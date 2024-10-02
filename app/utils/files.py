from typing import List
import os


if os.name == "nt":
    sep = "\\"
else:
    sep = "/"

files_path = f"{os.getcwd()}{sep}files"


def get_files_list() -> List[str]:
    files = os.listdir(files_path)
    files = list(filter(lambda x: x != ".gitignore", files))
    return files


def get_file_path(file) -> str:
    return f"{files_path}{sep}{file}"
