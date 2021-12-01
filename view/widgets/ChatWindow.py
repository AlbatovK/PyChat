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
            if messages is not None:
                for msg in messages:
                    self.messages_list.addItem(msg)

        observer = Observer(on_messages_changed)
        self.viewModel.messagesLive.add_observer(observer)

        for user in self.viewModel.users:
            self.users_list.addItem(user.nickname)

        def on_click(item: QListWidgetItem):
            self.viewModel.set_to_user(item.text())
            self.messages_list.clear()
            self.viewModel.fulfil_messages()

        self.users_list.itemClicked.connect(on_click)

        def on_send():
            data = self.msg_input.text()
            self.viewModel.send_msg(data)
            self.messages_list.clear()
            self.viewModel.fulfil_messages()

        self.send_btn.clicked.connect(on_send)
