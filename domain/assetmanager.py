from os import path

from domain.jsonparser import parse_from_file


def get_layout_path(filename: str):
    if not filename.endswith(".ui"):
        raise FileNotFoundError
    return path.dirname(__file__)[:-6:] + "layout" + "\\" + filename


def get_drawable_path(filename: str):
    return path.dirname(__file__)[:-6:] + "drawable" + "\\" + filename


def get_config():
    src = path.dirname(__file__)[:-6:] + "firebase-config.json"
    with open(src, 'r') as config_file:
        return parse_from_file(config_file)
