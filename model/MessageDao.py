from pyrebase.pyrebase import Firebase

from domain.jsonparser import parse_messages
from model.Message import Message
from model.User import User


class MessageDao:

    def __init__(self, firebase: Firebase):
        self.db = firebase.database()

    def insert_message(self, from_user: User, message: Message):
        msg = message.__dict__
        self.db.child("users").child(from_user.id).child("messages").push(msg)

    def get_messages(self, user: User):
        try:
            messages = self.db.child("users").child(user.id).child("messages").get()
            return parse_messages(messages)
        except TypeError:
            return []
