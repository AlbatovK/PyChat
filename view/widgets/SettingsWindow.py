from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from domain.assetmanager import get_layout_path
from model.ThemeEnum import Theme
from view.widgets.viewmodel.SettingsViewModel import SettingsViewModel


class SettingsWindow(QMainWindow):

    close_signal = pyqtSignal()

    def __init__(self, close_signal):
        super().__init__()
        self.viewModel = SettingsViewModel()
        self.current_theme = None

        self.close_signal = close_signal

        self.init_ui()

    def init_ui(self):
        uic.loadUi(get_layout_path("settings.ui"), self)
        self.setFixedSize(600, 500)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        def close():
            self.destroy(True, True)
            self.close_signal.emit()

        self.close_btn.clicked.connect(close)

        index = self.combo_box.findText("Тёмная" if self.viewModel.current_theme == Theme.DARK else "Светлая")
        self.combo_box.setCurrentIndex(index)

        def chosen_option():

            choose_dict = {
                "Тёмная": Theme.DARK,
                "Светлая": Theme.LIGHT
            }

            choice = self.combo_box.currentText()
            self.current_theme = choose_dict.get(choice, Theme.DARK)

        self.combo_box.currentIndexChanged.connect(chosen_option)

        def save_settings():
            if self.current_theme is not None:
                self.viewModel.save_settings(self.current_theme)

        self.apply_btn.clicked.connect(save_settings)

        def on_refresh_clicked():
            self.viewModel.refresh_current_user()

        self.refresh_btn.clicked.connect(on_refresh_clicked)

        def change_user():
            self.viewModel.change_user()
            self.destroy(True, True)

        self.change_btn.clicked.connect(change_user)
