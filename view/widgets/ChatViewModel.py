import time
from threading import Thread

from model.MainRepo import mainRepo
from model.Message import Message
from model.MessageDao import MessageDao
from model.UserDao import UserDao
from view.mvvm.LiveData import LiveData


class ChatViewModel(object):

    def __init__(self):
        self.firebase = mainRepo.provide_firebase_instance()
        self.user_dao = UserDao(self.firebase)
        self.msg_dao = MessageDao(self.firebase)
        self.users = []
        for user in self.user_dao.get_all_users():
            if not user.nickname == mainRepo.provide_current_user().nickname:
                self.users.append(user)
        self.messagesLive = LiveData([])
        self.to_user = None

        self.update_thread = Thread(target=self.update_screen)
        self.update_thread.start()

    def update_screen(self):
        while True:
            time.sleep(3)
            self.fulfil_messages()

    def set_to_user(self, nickname):
        print(nickname)
        for user in self.users:
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
