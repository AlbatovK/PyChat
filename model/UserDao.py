class UserDao:

    def __init__(self, firebase):
        self.db = firebase.database()

    def insert_user(self, user):
        self.db.child("users").child(user.nickname).set(user.id)
