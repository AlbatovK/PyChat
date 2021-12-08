from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from domain.assetmanager import get_layout_path
from domain.stringextensions import error_to_hint
from view.mvvm.Observer import Observer
from view.widgets.ChatWindow import ChatWindow
from view.widgets.viewmodel.EnteringViewModel import EnteringViewModel


class EnteringWindow(QMainWindow):

    request_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.viewModel = EnteringViewModel()

        self.init_view_model()
        self.init_ui()

    def init_view_model(self):

        def on_finished():
            self.close()
            self.chat_window = ChatWindow()
            self.chat_window.show()

        self.request_finished.connect(on_finished)

        def on_invalid_input(msg):
            hint = error_to_hint(msg)
            self.error_label.setText(hint)

        invalid_input_observer = Observer(on_invalid_input)
        self.viewModel.invalid_inputLive.add_observer(invalid_input_observer)

    def init_ui(self):
        uic.loadUi(get_layout_path("enter.ui"), self)
        self.setFixedSize(500, 540)

        self.sign_in_btn.clicked.connect(self.sign_in)
        self.sign_up_btn.clicked.connect(self.sign_up)
        self.login_input.cursorPositionChanged.connect(lambda: self.error_label.setText(''))
        self.password_input.cursorPositionChanged.connect(lambda: self.error_label.setText(''))

    def sign_in(self):
        login, password = self.login_input.toPlainText(), self.password_input.toPlainText()
        self.viewModel.sign_in_threaded(login, password, self.request_finished)

    def sign_up(self):
        login, password = self.login_input.toPlainText(), self.password_input.toPlainText()
        self.viewModel.sign_up_threaded(login, password, self.request_finished)
