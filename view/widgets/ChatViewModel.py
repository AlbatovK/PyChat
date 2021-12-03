import time
from datetime import datetime
from threading import Thread

from model.MainRepo import mainRepo
from model.Message import Message
from model.MessageDao import MessageDao
from model.User import User
from model.UserDao import UserDao
from view.mvvm.LiveData import LiveData

DELTA_USER_UPDATE_SEC = 20.0
DELTA_MSGS_UPDATE_SEC = 3.0


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
            time.sleep(DELTA_MSGS_UPDATE_SEC)
            self.fulfil_messages()

    def set_to_user(self, nickname):
        for user in self.usersLive.get_value():
            if nickname == user.nickname:
                self.to_user = user
                break

    def fulfil_messages(self):
        if self.to_user is not None:
            valid = []

            messages = self.msg_dao.get_messages(self.to_user)
            valid_his = [msg for msg in messages if msg.to_id == mainRepo.provide_current_user().id]
            valid.extend(valid_his)

            my_messages = self.msg_dao.get_messages(mainRepo.provide_current_user())
            valid_my = [msg for msg in my_messages if msg.to_id == self.to_user.id]
            valid.extend(valid_my)

            for msg in valid:
                msg.date = datetime.strptime(msg.date, "%a %b %d %H:%M:%S %Y")
            valid.sort(key=lambda x: x.date)
            res = list(map(lambda x: x.data, valid))

            if len(res) == 0:
                res.append("Начните диалог первым!")

            self.messagesLive.set_value(res)

    def send_msg(self, data):
        message = Message(data, self.to_user.id, time.ctime())
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
                res = [User("Поиск других аккаунтов", 0)]
            self.usersLive.set_value(res)
        except TypeError:
            self.usersLive.set_value([])

    def update_users_list(self):
        while True:
            self.set_users_list()
            time.sleep(DELTA_USER_UPDATE_SEC)

    def stop(self):
        self.update_thread_users.join(0)
        self.update_thread_msg.join(0)

    def update_user_status(self):
        self.user_dao.update_user_status(mainRepo.provide_current_user(), False)
