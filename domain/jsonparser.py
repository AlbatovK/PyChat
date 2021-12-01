import json

from requests import HTTPError


def parse_error_response(e: HTTPError):
    return str(e.errno).split()[0], json.loads(e.strerror)["error"]["message"].split()[0]


def parse_from_file(read_file):
    return json.load(read_file)
