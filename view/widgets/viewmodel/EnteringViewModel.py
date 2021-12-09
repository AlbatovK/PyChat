from threading import Thread

from requests import HTTPError

from domain.jsonparser import parse_error_response
from model.ThemeEnum import Theme
from model.dao.SettingsDao import SettingsDao
from model.repo.MainRepo import mainRepo
from model.User import User
from model.dao.UserDao import UserDao
from view.mvvm.LiveData import LiveData


class EnteringViewModel(object):

    def __init__(self):
        firebase = mainRepo.provide_firebase_instance()
        self.auth = firebase.auth()
        self.dao = UserDao(firebase)
        self.settings_dao = SettingsDao(firebase)

        self.invalid_inputLive = LiveData()

    def sign_in(self, login, password, signal_finish):
        try:
            user = self.auth.sign_in_with_email_and_password(login + "@gmail.com", password)
            user = self.auth.refresh(user['refreshToken'])
            self.create_and_save_user(login, user)
            signal_finish.emit()
        except HTTPError as e:
            code, msg = parse_error_response(e)
            self.invalid_inputLive.data = msg
            print(code, msg)

    def sign_in_threaded(self, login, password, signal_finish):
        Thread(target=self.sign_in, args=[login, password, signal_finish], daemon=False).start()

    def sign_up(self, login, password, signal_finish):
        try:
            user = self.auth.create_user_with_email_and_password(login + "@gmail.com", password)
            user = self.auth.refresh(user['refreshToken'])
            user = self.create_and_save_user(login, user)
            self.settings_dao.save_theme(user, Theme.DARK)
            signal_finish.emit()
        except HTTPError as e:
            code, msg = parse_error_response(e)
            self.invalid_inputLive.data = msg
            print(code, msg)

    def sign_up_threaded(self, login, password, signal_finish):
        Thread(target=self.sign_up, args=[login, password, signal_finish], daemon=False).start()

    def create_and_save_user(self, login, user: dict) -> User:
        user_impl = User(login, user["userId"], active=True)
        mainRepo.set_current_user(user_impl)
        mainRepo.set_current_firebase_user(user)
        self.dao.insert_user(user_impl)
        return user_impl
