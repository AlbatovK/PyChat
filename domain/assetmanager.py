from os import path

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon

from domain.jsonparser import parse_from_file

config_name, layout_dir, drawable_dir, assets_dir = "firebase-config.json", "layout", "drawable", "assets"

db_dir = "data"


def get_layout_path(filename: str) -> str:
    if not filename.endswith(".ui"):
        raise FileNotFoundError
    return path.dirname(__file__)[:-6:] + layout_dir + "\\" + filename


def get_drawable_path(filename: str) -> str:
    return path.dirname(__file__)[:-6:] + drawable_dir + "\\" + filename


def get_assets_path(filename: str) -> str:
    return path.dirname(__file__)[:-6:] + assets_dir + "\\" + filename


def get_database_path(filename: str) -> str:
    return path.dirname(__file__)[:-6:] + db_dir + "\\" + filename


def get_config() -> str:
    src = get_assets_path(config_name)
    with open(src, 'r') as config_file:
        return parse_from_file(config_file)


def load_theme(theme_file: str) -> str:
    file = QFile(theme_file)
    file.open(QFile.ReadOnly | QFile.Text)
    return QTextStream(file).readAll()


def get_icon(filename):
    name = get_drawable_path(filename)
    return QIcon(name)
