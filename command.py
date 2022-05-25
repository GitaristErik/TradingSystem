import abc


class Command:
    def __init__(self, controller):
        self.controller = controller

    @abc.abstractmethod
    def execute(self):
        pass
