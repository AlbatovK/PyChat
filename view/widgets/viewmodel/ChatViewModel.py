import time
from threading import Thread

from PyQt5.QtWidgets import QApplication

from domain.assetmanager import load_theme
from model.Message import Message
from model.ThemeEnum import Theme
from model.User import User
from model.dao.MessageDao import MessageDao
from model.dao.SettingsDao import SettingsDao
from model.dao.UserDao import UserDao
from model.repo.MainRepo import mainRepo
from model.repo.SettingsRepo import settings_repo
from view.mvvm.LiveData import LiveData

DELTA_USER_UPDATE_SEC = 20.0
DELTA_MSGS_UPDATE_SEC = 3.0


class ChatViewModel(object):

    def __init__(self):
        self.firebase = mainRepo.provide_firebase_instance()
        self.current_user = mainRepo.provide_current_user()
        self.user_dao = UserDao(self.firebase)
        self.msg_dao = MessageDao(self.firebase)
        self.settings_dao = SettingsDao(self.firebase)

        self.usersLive = LiveData()
        self.messagesLive = LiveData()

        self.messages = []
        self.to_user = None
        self.active = True

        self.set_users_list()

        self.update_thread_msg = Thread(target=self.update_msg_list)
        self.update_thread_msg.start()

        self.update_thread_users = Thread(target=self.update_users_list)
        self.update_thread_users.start()

    def load_theme(self):

        def load_light_theme():
            style_sheet = load_theme(":/light/stylesheet.qss")
            QApplication.instance().setStyleSheet(style_sheet)

        def load_dark_theme():
            style_sheet = load_theme(":/dark/stylesheet.qss")
            QApplication.instance().setStyleSheet(style_sheet)

        theme = self.settings_dao.get_current_theme(self.current_user)
        settings_repo.set_common_theme(theme)
        load_light_theme() if theme == Theme.LIGHT else load_dark_theme()

    def update_msg_list(self):
        while self.active:
            time.sleep(DELTA_MSGS_UPDATE_SEC)
            self.fulfil_messages()

    def set_to_user(self, nickname):
        for user in self.usersLive.data:
            if nickname == user.nickname:
                self.to_user = user
                self.messages.clear()
                break

    def get_messages(self):
        valid = []

        his = self.msg_dao.get_messages(self.to_user, self.current_user)
        valid.extend(his)

        my = self.msg_dao.get_messages(self.current_user, self.to_user)
        valid.extend(my)

        valid.sort(key=lambda x: x.date)

        return valid

    def archive_messages(self, file_name: str):
        if not file_name or not self.to_user:
            return

        def archive():
            with open(file_name, "w", encoding="utf-8", newline="\n") as file:
                msgs = self.get_messages()
                my = self.msg_dao.get_messages(self.current_user, self.to_user)

                for msg in msgs:
                    file.write(
                        f"{msg.data} ; "
                        f"{self.current_user.nickname if msg in my else self.to_user.nickname} ; "
                        f"{msg.date}"
                        "\n"
                    )

        Thread(target=archive, daemon=True).start()

    def fulfil_messages(self):
        if self.to_user is not None:
            msgs = self.get_messages()
            res = list(map(lambda x: x.data, msgs))

            if len(res) == 0:
                self.messagesLive.data = []
            else:
                self.messagesLive.data = res[len(self.messages): len(res)]
                self.messages = [msg for msg in res]

    def send_msg(self, data):
        message = Message(data, time.ctime())
        self.msg_dao.insert_message(self.current_user, self.to_user, message)
        self.messagesLive.data = self.messagesLive.data.append(data)

    def is_sending_enabled(self):
        return self.to_user is not None

    def set_users_list(self):
        all_lst, current = self.user_dao.get_all_users(), mainRepo.provide_current_user().nickname
        res = [x for x in all_lst if not x.nickname == current]

        if len(res) == 0:
            hint = User("Поиск других аккаунтов", 0, active=True)
            res = [hint]

        res = sorted(res, key=lambda x: x.active, reverse=True)
        self.usersLive.data = res

    def update_users_list(self):
        while self.active:
            self.set_users_list()
            time.sleep(DELTA_USER_UPDATE_SEC)

    def update_user_status(self):
        self.user_dao.update_user_status(mainRepo.provide_current_user(), False)

    def get_current_user(self):
        return self.current_user

    def stop_updating(self):
        self.active = False
