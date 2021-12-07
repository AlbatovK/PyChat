from os import path

from domain.jsonparser import parse_from_file

config_name = "firebase-config.json"
layout_dir = "layout"
drawable_dir = "drawable"


def get_layout_path(filename: str) -> str:
    if not filename.endswith(".ui"):
        raise FileNotFoundError
    return path.dirname(__file__)[:-6:] + layout_dir + "\\" + filename


def get_drawable_path(filename: str) -> str:
    return path.dirname(__file__)[:-6:] + drawable_dir + "\\" + filename


def get_config() -> str:
    src = path.dirname(__file__)[:-6:] + config_name
    with open(src, 'r') as config_file:
        return parse_from_file(config_file)
