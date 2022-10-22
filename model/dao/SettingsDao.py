import sqlite3

from pyrebase.pyrebase import Firebase

from domain.assetmanager import get_database_path
from model.ThemeEnum import Theme
from model.User import User


class SettingsDao:

    get_theme_dict = {
        "dark": Theme.DARK,
        "light": Theme.LIGHT
    }

    put_theme_dict = {
        Theme.LIGHT: 1,
        Theme.DARK: 0
    }

    db_path = get_database_path("prefs_db.sqlite")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    def __init__(self, firebase: Firebase):
        pass

    def save_theme(self, user: User, theme: Theme):
        theme_id = self.put_theme_dict.get(theme, 0)
        self.cursor.execute(f"UPDATE prefs SET mode_id = {theme_id} WHERE id = 1").fetchall()
        self.connection.commit()

    def get_current_theme(self, user: User):
        cmd = "SELECT modes.name FROM prefs INNER JOIN modes ON prefs.mode_id == modes.id"
        res = self.cursor.execute(cmd).fetchall()
        return self.get_theme_dict.get(res[0][0], Theme.DARK)

    def close(self):
        self.cursor.close()
        self.connection.close()
