from PyQt5.QtWidgets import QApplication

from domain.assetmanager import load_theme
from model.ThemeEnum import Theme
from model.dao.SettingsDao import SettingsDao
from model.repo.MainRepo import mainRepo
from model.repo.SettingsRepo import settings_repo


class SettingsViewModel:

    def __init__(self):
        self.firebase = mainRepo.provide_firebase_instance()
        self.current_user = mainRepo.provide_current_user()
        self.settings_dao = SettingsDao(self.firebase)
        self.current_theme = settings_repo.provide_common_theme()

    def save_settings(self, theme: Theme):
        self.current_theme = theme
        settings_repo.set_common_theme(theme)
        self.settings_dao.save_theme(self.current_user, theme)

        def load_light_theme():
            style_sheet = load_theme(":/light/stylesheet.qss")
            QApplication.instance().setStyleSheet(style_sheet)

        def load_dark_theme():
            style_sheet = load_theme(":/dark/stylesheet.qss")
            QApplication.instance().setStyleSheet(style_sheet)

        load_light_theme() if self.current_theme == Theme.LIGHT else load_dark_theme()
