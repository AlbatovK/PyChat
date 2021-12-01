import sys

from PyQt5.QtWidgets import QApplication
from pyrebase import pyrebase

from domain.assetmanager import get_config
from model.MainRepo import mainRepo
from view.widgets.EnteringWindow import EnteringWindow


def establish_firebase():
    firebase_config = get_config()
    return pyrebase.initialize_app(firebase_config)


if __name__ == "__main__":
    firebase = establish_firebase()
    mainRepo.firebase_instance = firebase
    app = QApplication(sys.argv)
    window = EnteringWindow()
    window.show()
    sys.exit(app.exec())
