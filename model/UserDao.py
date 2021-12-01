from pyrebase.pyrebase import Firebase

from model.Message import Message
from model.User import User


class UserDao:

    def __init__(self, firebase: Firebase):
        self.db = firebase.database()

    def insert_user(self, user: User):
        self.db.child("users").child(user.id).child("nickname").set(user.nickname)

    def insert_message(self, from_user: User, message: Message):
        msg = message.__dict__
        self.db.child("users").child(from_user.id).child("messages").push(msg)
