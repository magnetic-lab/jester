# -*- coding: utf-8 -*-
"""General Utilities"""
import os
from collections import namedtuple
import importlib.metadata
import logging

from ffprobe import FFProbe
import yaml


def setup_logger():
    logger = logging.getLogger("jester")
    logger.setLevel(logging.DEBUG)
    return logger

LOGGER = setup_logger()

def data_from_directory(directory_path):
    """Retreive data from target directory.

    Args:
        directory_path (directory_path): path to directory containing media to injest.

    Returns:
        dict: dictionary created from data in yaml file.
    """
    data = {}
    for dir_entry in os.scandir(directory_path):
        if dir_entry.is_file() and is_media(dir_entry.path):
            print(f"found media: {dir_entry.path}")
        elif dir_entry.is_dir():
            data = data_from_directory(dir_entry.path)
            

def data_from_yaml(filepath):
    """Retreive data from target yaml filepath.

    Args:
        filepath (filepath): valid path to yaml file.

    Returns:
        dict: dictionary created from data in yaml file.
    """
    data = {}
    with open(filepath, 'r') as fobj:
        data = yaml.safe_load(fobj)
    return data


def get_package_metadata():
    """Retreive metadata from current `pip` package.

    Returns:
        dict: dictionary containing metadata from package definition (setup.py).
    """
    return importlib.metadata.metadata("jester")

def metadata_from_filepath(filepath):
    return FFProbe(filepath)

def is_media(filepath):
    return os.path.isfile(filepath) and filepath.endswith(".mp4")