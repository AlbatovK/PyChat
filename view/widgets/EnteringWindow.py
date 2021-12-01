from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from domain.assetmanager import get_layout_path, get_drawable_path
from domain.stringextensions import error_to_hint
from view.mvvm.Observer import Observer
from view.widgets.ChatWindow import ChatWindow
from view.widgets.EnteringViewModel import EnteringViewModel


class EnteringWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.viewModel = EnteringViewModel()

        def on_user_loaded(_):
            self.chat_window = ChatWindow()
            self.chat_window.show()

        user_loaded_observer = Observer(on_user_loaded)
        self.viewModel.userLive.add_observer(user_loaded_observer)

        def on_invalid_input(msg):
            hint = error_to_hint(msg)
            self.error_label.setText(hint)

        invalid_input_observer = Observer(on_invalid_input)
        self.viewModel.invalid_inputLive.add_observer(invalid_input_observer)
        self.init_ui()

    def init_ui(self):
        uic.loadUi(get_layout_path("enter.ui"), self)
        pixmap = QPixmap(get_drawable_path("icon.png"))
        self.logo_label.setPixmap(pixmap)

        self.sign_in_btn.clicked.connect(self.sign_in)
        self.sign_up_btn.clicked.connect(self.sign_up)
        self.login_input.cursorPositionChanged.connect(lambda: self.error_label.setText(''))
        self.password_input.cursorPositionChanged.connect(lambda: self.error_label.setText(''))

    def sign_in(self):
        login, password = self.login_input.toPlainText(), self.password_input.toPlainText()
        self.viewModel.sign_in(login, password)

    def sign_up(self):
        login, password = self.login_input.toPlainText(), self.password_input.toPlainText()
        self.viewModel.sign_up(login, password)
