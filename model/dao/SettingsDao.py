from pyrebase.pyrebase import Firebase

from model.ThemeEnum import Theme
from model.User import User


class SettingsDao:

    get_theme_dict = {
        "light": Theme.LIGHT,
        "dark": Theme.DARK
    }

    put_theme_dict = {
        Theme.LIGHT: "light",
        Theme.DARK: "dark"
    }

    def __init__(self, firebase: Firebase):
        self.__db = firebase.database()

    def save_theme(self, user: User, theme: Theme):
        data = self.put_theme_dict.get(theme, "dark")
        self.__db.child("users").child(user.id).child("settings").child("def_theme").set(data)

    def get_current_theme(self, user: User):
        data = self.__db.child("users").child(user.id).child("settings").child("def_theme").get().val()
        return self.get_theme_dict.get(data, Theme.DARK)
