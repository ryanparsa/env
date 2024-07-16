import logging
import os
import sys
from io import TextIOWrapper, IOBase, TextIOBase, FileIO, StringIO

from typing import AnyStr, IO, TextIO, Union, Any, Mapping, Dict, TypedDict


# TODO: handle os.PathLike


def env_file_path_loader(file_path: str, mode: str = 'r', encoding: str = "utf-8", replace: bool = True) -> None:
    if os.path.exists(file_path):
        logging.debug(f'loading {file_path}')
        return env_file_io_loader(file=open(file_path, mode, encoding=encoding), replace=replace)

    logging.error(f"File {file_path} does not exist!")


def env_file_io_loader(file: TextIO, replace: bool = True) -> None:
    for line in file:
        if not line.startswith("#"):
            key, value = line.split("=")
            if replace:
                os.environ[key] = value
            else:
                os.environ.setdefault(key, value)
            logging.debug(f"Environment variable {key}={value} added")


def env_dict_loader(data: dict[str, Any], replace: bool = True):
    if replace:
        os.environ.update(data)

    else:
        for key, value in data.items():
            os.environ.setdefault(key, value)

    logging.debug(f"Environment variable {data} loaded")


def find_env_files():
    """
    Find all files in the current directory containing 'env' in their filename.

    Returns:
    - list: List of filenames containing 'env'.
    """
    current_dir = os.getcwd()
    env_files = []

    logging.debug(f"Current directory: {current_dir}")

    for file in os.listdir(current_dir):
        if file.find('env') > 0 and os.path.isfile(file):
            env_files.append(file)

    logging.debug(f"Found {len(env_files)} env files")
    return env_files


def env(*args: Any | None, replace: bool = True):
    if os.getenv('ENV_LOADED'):
        logging.debug(f"Environment variable already loaded. running again")

    if not args:
        logging.debug(f'args is empty, auto loading ')
        args = find_env_files()

    for arg in args:
        if isinstance(arg, str):
            env_file_path_loader(arg, replace=replace)
        elif isinstance(arg, dict):
            env_dict_loader(arg, replace=replace)
        elif isinstance(arg, TextIO):
            env_file_io_loader(arg, replace=replace)

    os.environ.setdefault("ENV_LOADED", '1')
    os.environ.setdefault("ENV_LOADED_ARGS", ', '.join(args))
