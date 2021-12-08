from datetime import datetime


class Message:

    def __init__(self, data: str, date: str):
        self.__data = data
        self.__date = date

    @property
    def data(self):
        return self.__data

    @data.getter
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: str):
        self.__data = data if not data.isspace() else "..."

    @property
    def date(self):
        return self.__date

    @date.getter
    def date(self) -> datetime:
        return datetime.strptime(self.__date, "%a %b %d %H:%M:%S %Y")

    @date.setter
    def date(self, date: str):
        self.__date = date

    def get_dict(self):
        return {"data": self.__data, "date": self.__date}
