from typing import List

from pyrebase.pyrebase import Firebase

from domain.jsonparser import parse_messages
from model.Message import Message
from model.User import User


class MessageDao:

    def __init__(self, firebase: Firebase):
        self.__db = firebase.database()

    def insert_message(self, from_user: User, to_user: User, message: Message) -> None:
        msg = message.get_dict()
        self.__db.child("users").child(from_user.id).child("messages").child(to_user.id).push(msg)

    def get_messages(self, from_user: User, to_user: User) -> List[Message]:
        messages = self.__db.child("users").child(from_user.id).child("messages").child(to_user.id).get()
        return parse_messages(messages) if messages.each() is not None else []
