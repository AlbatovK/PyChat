import time
from threading import Thread

from model.MainRepo import mainRepo
from model.Message import Message
from model.MessageDao import MessageDao
from model.User import User
from model.UserDao import UserDao
from view.mvvm.LiveData import LiveData

DELTA_SEC = 3.0


class ChatViewModel(object):

    def __init__(self):
        self.firebase = mainRepo.provide_firebase_instance()
        self.user_dao = UserDao(self.firebase)
        self.msg_dao = MessageDao(self.firebase)
        self.usersLive = LiveData()
        self.messagesLive = LiveData()
        self.to_user = None

        self.set_users_list()

        self.update_thread_msg = Thread(target=self.update_msg_list)
        self.update_thread_msg.start()

        self.update_thread_users = Thread(target=self.update_users_list)
        self.update_thread_users.start()

    def update_msg_list(self):
        while True:
            time.sleep(DELTA_SEC)
            self.fulfil_messages()

    def set_to_user(self, nickname):
        print(nickname)
        for user in self.usersLive.get_value():
            if nickname == user.nickname:
                self.to_user = user
                break

    def fulfil_messages(self):
        if self.to_user is not None:
            messages = self.msg_dao.get_messages(self.to_user)
            res = []

            for msg in messages:
                if msg.to_id == mainRepo.provide_current_user().id:
                    res.append(msg.data)

            my_messages = self.msg_dao.get_messages(mainRepo.provide_current_user())

            for msg in my_messages:
                if msg.to_id == self.to_user.id:
                    res.append(msg.data)

            if len(res) == 0:
                res.append("Начните диалог первым!")
            self.messagesLive.set_value(res)

    def send_msg(self, data):
        message = Message(data, self.to_user.id)
        self.msg_dao.insert_message(mainRepo.provide_current_user(), message)
        self.messagesLive.set_value(self.messagesLive.get_value().append(data))

    def is_sending_enabled(self):
        return self.to_user is not None

    def set_users_list(self):
        try:
            res = []
            for user in self.user_dao.get_all_users():
                if not user.nickname == mainRepo.provide_current_user().nickname:
                    res.append(user)
            if len(res) == 0:
                res = [User("Поиск других аккаунтов", 123)]
            self.usersLive.set_value(res)
        except TypeError:
            self.usersLive.set_value([])

    def update_users_list(self):
        while True:
            time.sleep(DELTA_SEC)
            self.set_users_list()
