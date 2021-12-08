from typing import List

from pyrebase.pyrebase import Firebase

from domain.jsonparser import parse_users
from model.User import User


class UserDao:

    def __init__(self, firebase: Firebase):
        self.__db = firebase.database()

    def insert_user(self, user: User) -> None:
        self.__db.child("users").child(user.id).child("nickname").set(user.nickname)
        self.__db.child("users").child(user.id).child("active").set(user.active)

    def update_user_status(self, user: User, active: bool) -> None:
        update_dict = {"active": True if active else False}
        self.__db.child("users").child(user.id).update(update_dict)

    def get_all_users(self) -> List[User]:
        all_users = self.__db.child("users").get()
        return parse_users(all_users) if all_users.each() is not None else []
