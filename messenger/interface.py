from multiprocessing import Queue, Event

from . graphics import mvc_interface, message_box, git_app, main_frame


class UI(mvc_interface.MVCInterface, message_box.MessageBoxApplication, git_app.GitApplication):

    def __init__(self, model):

        super().__init__(model=model)