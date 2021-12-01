class MainRepo:

    def __init__(self):
        self.firebase_instance, self.current_user = None, None
        self.user_impl, self.to_user = None, None

    def provide_firebase_instance(self):
        return self.firebase_instance

    def provide_current_user(self):
        return self.current_user


mainRepo: MainRepo = MainRepo()
