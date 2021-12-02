class MainRepo:

    def __init__(self):
        self.firebase_instance, self.user_impl = None, None

    def provide_firebase_instance(self):
        if self.firebase_instance is None:
            raise RuntimeError("Data is not initialized")
        return self.firebase_instance

    def provide_current_user(self):
        if self.user_impl is None:
            raise RuntimeError("Data is not initialized")
        return self.user_impl

    def set_current_user(self, user):
        self.user_impl = user

    def initialize(self, firebase):
        self.firebase_instance = firebase


mainRepo: MainRepo = MainRepo()
