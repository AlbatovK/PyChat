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

    def get_all_users(self):
        res = []
        all_users = self.db.child("users").get()
        for item in all_users.each():
            user = User(item.val()['nickname'], item.key())
            res.append(user)
        return res

    def get_messages(self, user: User):
        res = []
        messages = self.db.child("users").child(user.id).child("messages").get()
        try:
            for item in messages.each():
                value = item.val()
                res.append(Message(value["data"], value["to_id"], value["date"]))
            return res
        except TypeError:
            return []
