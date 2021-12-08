from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QComboBox

from domain.assetmanager import get_layout_path
from model.ThemeEnum import Theme
from view.widgets.viewmodel.SettingsViewModel import SettingsViewModel


class SettingsWindow(QMainWindow):

    def __init__(self, close_signal):
        super().__init__()
        self.viewModel = SettingsViewModel()

        self.close_signal = close_signal

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.init_ui()

    def init_ui(self):
        uic.loadUi(get_layout_path("settings.ui"), self)
        self.setFixedSize(600, 500)

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
            self.viewModel.save_settings(self.current_theme)

        self.apply_btn.clicked.connect(save_settings)
