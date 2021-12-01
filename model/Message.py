import time


class Message(object):

    def __init__(self, data, to_id, date=time.ctime()):
        self.data = data
        self.to_id = to_id
        self.date = date
