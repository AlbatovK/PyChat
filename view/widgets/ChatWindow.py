from PyQt5 import uic, QtCore
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem

from domain.assetmanager import get_layout_path, get_icon
from model.dao.SettingsDao import SettingsDao
from view.mvvm.Observer import Observer
from view.widgets.viewmodel.ChatViewModel import ChatViewModel
from view.widgets.SettingsWindow import SettingsWindow

MAX_LINE_LENGTH = 40


class ChatWindow(QMainWindow):

    show_request = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.viewModel = ChatViewModel()

        self.init_ui()

    def init_ui(self):
        uic.loadUi(get_layout_path("chat.ui"), self)
        self.setFixedSize(800, 600)
        self.viewModel.load_theme()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        exit_ic, refresh_ic = get_icon("exit.png"), get_icon("refresh.png")
        settings_ic, send_ic = get_icon("settings.png"), get_icon("send.png")
        avg_size, send_size = QSize(25, 25), QSize(30, 30)

        self.exit_btn.setIcon(exit_ic)
        self.exit_btn.setIconSize(avg_size)
        self.refresh_btn.setIcon(refresh_ic)
        self.refresh_btn.setIconSize(avg_size)
        self.settings_btn.setIcon(settings_ic)
        self.settings_btn.setIconSize(avg_size)
        self.send_btn.setIcon(send_ic)
        self.send_btn.setIconSize(send_size)

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
            online_ic, not_online_ic = get_icon("online"), get_icon("not_online")

            for item in users:
                icon = online_ic if item.active else not_online_ic
                q_item = QListWidgetItem(icon, item.nickname)
                self.users_list.addItem(q_item)

        users_changed = Observer(on_users_changed)
        self.viewModel.usersLive.add_observer(users_changed)

        def on_click(item: QListWidgetItem):
            self.viewModel.set_to_user(item.text())
            self.messages_list.clear()
            self.viewModel.fulfil_messages()

        self.users_list.itemClicked.connect(on_click)

        def on_send():
            data = self.msg_input.text()
            self.msg_input.clear()
            if self.viewModel.is_sending_enabled() and not data == '':
                self.viewModel.send_msg(data)
                self.viewModel.fulfil_messages()
                self.messages_list.scrollToBottom()

        self.send_btn.clicked.connect(on_send)

        def refresh_users():
            self.viewModel.set_users_list()

        self.refresh_btn.clicked.connect(refresh_users)

        def exit_app():
            self.viewModel.update_user_status()
            self.destroy(True, True)

        self.exit_btn.clicked.connect(exit_app)

        def show_settings():
            self.hide()
            self.settings_dialog = SettingsWindow(self.show_request)
            self.settings_dialog.show()

        self.settings_btn.clicked.connect(show_settings)

        self.show_request.connect(self.show)

        self.viewModel.set_users_list()
