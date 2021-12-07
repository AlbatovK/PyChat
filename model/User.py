class User:

    def __init__(self, nickname, _id, active=False):
        self.__nickname = nickname
        self.__id = _id
        self.__active = active

    @property
    def nickname(self):
        return self.__nickname

    @nickname.getter
    def nickname(self):
        return self.__nickname

    @nickname.setter
    def nickname(self, nickname: str):
        if nickname.isspace():
            raise RuntimeError("Username must not be empty")

    @property
    def id(self):
        return self.__id

    @id.getter
    def id(self):
        return self.__id

    @property
    def active(self):
        return self.__active

    @active.getter
    def active(self):
        return self.__active

    @active.setter
    def active(self, active):
        self.__active = active
