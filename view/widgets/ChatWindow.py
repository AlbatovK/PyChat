from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from domain.assetmanager import get_layout_path


class ChatWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(get_layout_path("chat.ui"))
