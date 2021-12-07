from PyQt5 import uic, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem

from domain.assetmanager import get_layout_path, get_drawable_path
from view.mvvm.Observer import Observer
from view.widgets.ChatViewModel import ChatViewModel

MAX_LINE_LENGTH = 40


class ChatWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.viewModel = ChatViewModel()
        self.init_ui()

    def init_ui(self):
        uic.loadUi(get_layout_path("chat.ui"), self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.exit_btn.setIcon(QIcon(get_drawable_path("exit.png")))
        self.exit_btn.setIconSize(QSize(25, 25))
        self.refresh_btn.setIcon(QIcon(get_drawable_path("refresh.png")))
        self.refresh_btn.setIconSize(QSize(25, 25))
        self.settings_btn.setIcon(QIcon(get_drawable_path("settings.png")))
        self.settings_btn.setIconSize(QSize(25, 25))
        self.send_btn.setIcon(QIcon(get_drawable_path("send.png")))
        self.send_btn.setIconSize(QSize(30, 30))

        def on_messages_changed(messages):
            if self.messages_list.count() == 1 and self.messages_list.item(0).text() == "Начните диалог первым!":
                self.messages_list.clear()

            if messages is not None:
                for msg in messages:
                    if len(msg) > MAX_LINE_LENGTH:
                        msg = msg[:MAX_LINE_LENGTH].strip() + "\n" + msg[MAX_LINE_LENGTH:].strip()
                    self.messages_list.addItem(msg)
                    self.messages_list.scrollToBottom()
                if not messages and self.messages_list.count() == 0:
                    self.messages_list.addItem("Начните диалог первым!")

        observer = Observer(on_messages_changed)
        self.viewModel.messagesLive.add_observer(observer)

        def on_users_changed(users):
            self.users_list.clear()

            for item in users:
                icon = QIcon(get_drawable_path("online")) if item.active else QIcon(get_drawable_path("not_online"))
                q_item = QListWidgetItem(icon, item.nickname)
                self.users_list.addItem(q_item)

        users_changed = Observer(on_users_changed)
        self.viewModel.usersLive.add_observer(users_changed)

        def on_click(item: QListWidgetItem):
            self.viewModel.set_to_user(item.text())
            self.messages_list.clear()
            self.viewModel.fulfil_messages_threaded()

        self.users_list.itemClicked.connect(on_click)

        def on_send():
            data = self.msg_input.text()
            self.msg_input.clear()
            if self.viewModel.is_sending_enabled() and not data == '':
                self.viewModel.send_msg_threaded(data)
                self.viewModel.fulfil_messages_threaded()
                self.messages_list.scrollToBottom()

        self.send_btn.clicked.connect(on_send)

        def refresh_users():
            self.viewModel.set_users_list_threaded()

        self.refresh_btn.clicked.connect(refresh_users)

        def exit_app():
            self.viewModel.update_user_status_threaded()
            self.viewModel.stop()
            self.destroy(True, True)

        self.exit_btn.clicked.connect(exit_app)

        def show_settings():
            # self.hide()
            self.window = QMainWindow()
            self.window.show()

        self.settings_btn.clicked.connect(show_settings)
