import json

from pyrebase.pyrebase import PyreResponse
from requests import HTTPError
from typing import List

from model.Message import Message
from model.User import User


def parse_error_response(e: HTTPError):
    return str(e.errno).split()[0], json.loads(e.strerror)["error"]["message"].split()[0]


def parse_from_file(read_file) -> str:
    return json.load(read_file)


def parse_messages(response: PyreResponse) -> List[Message]:

    def parse_single(item: PyreResponse) -> Message:
        return Message(item.val()["data"], item.val()["date"])

    map_query = map(parse_single, response.each())
    return list(map_query)


def parse_users(response: PyreResponse) -> List[User]:

    def parse_single(item: PyreResponse):
        return User(item.val()['nickname'], item.key(), True if str(item.val()['active']) == "True" else False)

    map_query = map(parse_single, response.each())
    return list(map_query)
