from pyrebase.pyrebase import Firebase

from model.User import User


class UserDao:

    def __init__(self, firebase: Firebase):
        self.db = firebase.database()

    def insert_user(self, user: User):
        self.db.child("users").child(user.id).child("nickname").set(user.nickname)

    def get_all_users(self):
        res = []
        all_users = self.db.child("users").get()
        for item in all_users.each():
            user = User(item.val()['nickname'], item.key())
            res.append(user)
        return res
