import json

from pyrebase.pyrebase import PyreResponse
from requests import HTTPError
from typing import List

from model.Message import Message


def parse_error_response(e: HTTPError):
    return str(e.errno).split()[0], json.loads(e.strerror)["error"]["message"].split()[0]


def parse_from_file(read_file) -> str:
    return json.load(read_file)


def parse_messages(response: PyreResponse) -> List[Message]:

    def parse_single(item: PyreResponse) -> Message:
        return Message(item.val()["data"], item.val()["date"])

    return list(map(parse_single, response.each()))
