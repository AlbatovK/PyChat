from requests import HTTPError

from domain.jsonparser import parse_error_response
from model.MainRepo import mainRepo
from model.User import User
from model.UserDao import UserDao
from view.mvvm.LiveData import LiveData


class EnteringViewModel(object):

    def __init__(self):
        self.userLive = LiveData()
        self.invalid_inputLive = LiveData()
        self.repo = mainRepo
        self.auth = mainRepo.firebase_instance.auth()
        self.dao = UserDao(mainRepo.firebase_instance)

    def sign_in(self, login, password):
        try:
            user = self.auth.sign_in_with_email_and_password(login + "@gmail.com", password)
            user = self.auth.refresh(user['refreshToken'])
            self.create_and_save_user(login, user)
        except HTTPError as e:
            code, msg = parse_error_response(e)
            self.invalid_inputLive.set_value(msg)
            print(code, msg)

    def sign_up(self, login, password):
        try:
            user = self.auth.create_user_with_email_and_password(login + "@gmail.com", password)
            user = self.auth.refresh(user['refreshToken'])
            self.create_and_save_user(login, user)
        except HTTPError as e:
            code, msg = parse_error_response(e)
            self.invalid_inputLive.set_value(msg)
            print(code, msg)

    def create_and_save_user(self, login, user):
        mainRepo.current_user = user
        mainRepo.user_impl = User(login, user["userId"])
        self.userLive.set_value(mainRepo.user_impl)
        self.dao.insert_user(mainRepo.user_impl)
