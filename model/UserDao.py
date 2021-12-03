from pyrebase.pyrebase import Firebase

from model.User import User


class UserDao:

    def __init__(self, firebase: Firebase):
        self.db = firebase.database()

    def insert_user(self, user: User):
        self.db.child("users").child(user.id).child("nickname").set(user.nickname)
        self.db.child("users").child(user.id).child("active").set(user.active)

    def update_user_status(self, user, active):
        update_dict = {"active": True if active else False}
        self.db.child("users").child(user.id).update(update_dict)

    def get_all_users(self):
        res = []
        all_users = self.db.child("users").get()
        for item in all_users.each():
            user = User(item.val()['nickname'], item.key(), True if str(item.val()['active']) == "True" else False)
            res.append(user)
        return res
