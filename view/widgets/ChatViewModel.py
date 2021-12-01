from model.MainRepo import mainRepo
from model.Message import Message
from model.UserDao import UserDao
from view.mvvm.LiveData import LiveData


class ChatViewModel(object):

    def __init__(self):
        self.firebase = mainRepo.firebase_instance
        self.dao = UserDao(self.firebase)
        self.users = self.dao.get_all_users()
        self.messagesLive = LiveData([])
        self.to_user = None

    def set_to_user(self, nickname):
        print(nickname)
        for user in self.users:
            if nickname == user.nickname:
                self.to_user = user
                break

    def fulfil_messages(self):
        if self.to_user is not None:
            messages = self.dao.get_messages(self.to_user)
            print(messages)
            res = []

            for msg in messages:
                print(msg.to_id, mainRepo.user_impl.id)
                if msg.to_id == mainRepo.user_impl.id:
                    res.append(msg.data)

            my_messages = self.dao.get_messages(mainRepo.user_impl)
            print(my_messages)

            for msg in my_messages:
                if msg.to_id == self.to_user.id:
                    res.append(msg.data)

            if len(res) == 0:
                res.append("Начните диалог первым!")
            self.messagesLive.set_value(res)

    def send_msg(self, data):
        message = Message(data, self.to_user.id)
        self.dao.insert_message(mainRepo.user_impl, message)
        self.messagesLive.set_value(self.messagesLive.get_value().append(data))
