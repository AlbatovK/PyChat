from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem

from domain.assetmanager import get_layout_path
from view.mvvm.Observer import Observer
from view.widgets.ChatViewModel import ChatViewModel


class ChatWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.viewModel = ChatViewModel()
        self.init_ui()

    def init_ui(self):
        uic.loadUi(get_layout_path("chat.ui"), self)

        def on_messages_changed(messages):
            self.messages_list.clear()
            if messages is not None:
                for msg in messages:
                    self.messages_list.addItem(msg)

        observer = Observer(on_messages_changed)
        self.viewModel.messagesLive.add_observer(observer)

        def on_users_changed(users):
            self.users_list.clear()
            for item in users:
                self.users_list.addItem(item.nickname + (" (online) " if item.active else " (not present) "))

        users_changed = Observer(on_users_changed)
        self.viewModel.usersLive.add_observer(users_changed)

        def on_click(item: QListWidgetItem):
            self.viewModel.set_to_user(item.text().replace(" (online) ", '').replace(" (not present) ", ""))
            self.messages_list.clear()
            self.viewModel.fulfil_messages()

        self.users_list.itemClicked.connect(on_click)

        def on_send():
            data = self.msg_input.text()
            self.msg_input.clear()
            if self.viewModel.is_sending_enabled():
                self.viewModel.send_msg(data)
                self.messages_list.clear()
                self.viewModel.fulfil_messages()

        self.send_btn.clicked.connect(on_send)

        def refresh_users():
            self.viewModel.set_users_list()

        self.refresh_btn.clicked.connect(refresh_users)

        def exit_app():
            self.viewModel.update_user_status()
            self.viewModel.stop()
            self.destroy(True, True)

        self.exit_btn.clicked.connect(exit_app)
