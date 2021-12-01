class LiveData:

    def __init__(self, data=''):
        self.data = data
        self.observers = []

    def get_value(self):
        return self.data

    def set_value(self, data):
        if not self == data:
            self.data = data
            for observer in self.observers:
                observer.callback(data)

    def add_observer(self, observer):
        self.observers.append(observer)
