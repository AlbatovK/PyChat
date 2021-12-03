import sys

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from pyrebase import pyrebase
import theme_resources
from domain.assetmanager import get_config
from model.MainRepo import mainRepo
from view.widgets.EnteringWindow import EnteringWindow


def establish_firebase():
    firebase_config = get_config()
    return pyrebase.initialize_app(firebase_config)


if __name__ == "__main__":
    firebase = establish_firebase()
    mainRepo.initialize(firebase)
    app = QApplication(sys.argv)

    file = QFile(":/dark/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    window = EnteringWindow()
    window.show()
    sys.exit(app.exec())
