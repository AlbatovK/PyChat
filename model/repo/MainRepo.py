from pyrebase.pyrebase import Firebase

from model.User import User


class MainRepo:

    def __init__(self):
        self.__firebase_instance, self.__user_impl, self.__firebase_user = None, None, None

    def provide_firebase_instance(self) -> Firebase:
        if self.__firebase_instance is None:
            raise RuntimeError("Data is not initialized")
        return self.__firebase_instance

    def provide_current_user(self) -> User:
        if self.__user_impl is None:
            raise RuntimeError("Data is not initialized")
        return self.__user_impl

    def set_current_user(self, user: User) -> None:
        self.__user_impl = user

    def set_current_firebase_user(self, user: dict):
        self.__firebase_user = user

    def provide_firebase_user(self) -> dict:
        if self.__firebase_user is None:
            raise RuntimeError("Data is not initialized")
        return self.__firebase_user

    def initialize(self, firebase: Firebase) -> None:
        if self.__firebase_instance is not None:
            raise RuntimeError("Double initializing")
        self.__firebase_instance = firebase


mainRepo: MainRepo = MainRepo()
