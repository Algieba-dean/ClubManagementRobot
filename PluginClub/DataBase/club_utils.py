class OutputMessageIterator:
    def __init__(self):
        self.message_list = list()

    def add_new_message(self, msg: str):
        self.message_list.append(msg)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.message_list) == 0:
            raise StopIteration
        return self.message_list.pop(0)
