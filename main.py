import sys

from PyQt5.QtWidgets import QApplication
from pyrebase import pyrebase
from domain.assetmanager import get_config, load_theme
from model.repo.MainRepo import mainRepo
from view.widgets.EnteringWindow import EnteringWindow
import app_theme_resources


def establish_firebase():
    firebase_config = get_config()
    return pyrebase.initialize_app(firebase_config)


def load_dark_theme(application: QApplication):
    style_sheet = load_theme(":/dark/stylesheet.qss")
    application.setStyleSheet(style_sheet)


if __name__ == "__main__":
    firebase = establish_firebase()
    mainRepo.initialize(firebase)
    app = QApplication(sys.argv)
    load_dark_theme(app)
    EnteringWindow().show()
    sys.exit(app.exec())
