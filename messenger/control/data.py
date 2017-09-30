import json

from utils.logger import Logger


class Data(Logger):
    def __init__(self, controller):

        self.controller = controller

        self.keys = ["network"]

        self.param = {}
        self.setup()

    def setup(self):

        for key in self.keys:
            # noinspection SpellCheckingInspection
            with open("parameters/{}.json".format(key)) as file:
                self.param[key] = json.load(file)

