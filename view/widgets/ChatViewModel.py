import time
from threading import Thread

from model.MainRepo import mainRepo
from model.Message import Message
from model.MessageDao import MessageDao
from model.User import User
from model.UserDao import UserDao
from view.mvvm.LiveData import LiveData

DELTA_USER_UPDATE_SEC = 60.0
DELTA_MSGS_UPDATE_SEC = 3.0


class ChatViewModel(object):

    def __init__(self):
        self.firebase = mainRepo.provide_firebase_instance()
        self.user_dao = UserDao(self.firebase)
        self.msg_dao = MessageDao(self.firebase)
        self.usersLive = LiveData([])
        self.messagesLive = LiveData()
        self.messages = []
        self.to_user = None
        self.current_user = mainRepo.provide_current_user()
        a: Message
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
        for user in self.usersLive.data:
            if nickname == user.nickname:
                self.to_user = user
                self.messages = []
                break

    def fulfil_messages(self):
        if self.to_user is not None:
            valid = []

            his = self.msg_dao.get_messages(self.to_user, self.current_user)
            valid.extend(his)

            my = self.msg_dao.get_messages(self.current_user, self.to_user)
            valid.extend(my)

            valid.sort(key=lambda x: x.date)
            res = list(map(lambda x: x.data, valid))

            if len(res) == 0:
                res.append("Начните диалог первым!")
                self.messagesLive.data = []
            else:
                self.messagesLive.data = res[len(self.messages): len(res)]
                self.messages = res.copy()

    def fulfil_messages_threaded(self):
        Thread(target=self.fulfil_messages, daemon=False).start()

    def send_msg(self, data):
        message = Message(data, time.ctime())
        self.msg_dao.insert_message(self.current_user, self.to_user, message)
        self.messagesLive.data = self.messagesLive.data.append(data)

    def send_msg_threaded(self, data):
        Thread(target=self.send_msg, args=[data], daemon=False).start()

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
            res = sorted(res, key=lambda x: x.active, reverse=True)
            self.usersLive.data = res
        except TypeError:
            self.usersLive.data = []

    def set_users_list_threaded(self):
        Thread(target=self.set_users_list, daemon=False).start()

    def update_users_list(self):
        while True:
            self.set_users_list()
            time.sleep(DELTA_USER_UPDATE_SEC)

    def stop(self):
        self.update_thread_users.join(0)
        self.update_thread_msg.join(0)

    def update_user_status(self):
        self.user_dao.update_user_status(mainRepo.provide_current_user(), False)

    def update_user_status_threaded(self):
        Thread(target=self.update_user_status, daemon=False).start()

    def get_current_user_name(self):
        return self.current_user.nickname
