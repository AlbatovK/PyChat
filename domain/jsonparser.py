import json

from pyrebase.pyrebase import PyreResponse
from requests import HTTPError

from model.Message import Message


def parse_error_response(e: HTTPError):
    return str(e.errno).split()[0], json.loads(e.strerror)["error"]["message"].split()[0]


def parse_from_file(read_file):
    return json.load(read_file)


def parse_messages(response: PyreResponse):

    def parse_single(item):
        value = item.val()
        return Message(value["data"], value["to_id"], value["date"])

    return list(map(parse_single, response.each()))
