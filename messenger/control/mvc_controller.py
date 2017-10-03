from multiprocessing import Queue, Event
from threading import Thread

from utils.logger import Logger

from messenger.control import data
from messenger.control import server


class MVCController(Thread, Logger):
    name = "Controller"

    def __init__(self, model):

        super().__init__()

        self.mod = model

        # For receiving inputs
        self.queue = Queue()

        self.shutdown = Event()

        self.data = data.Data(controller=self)
        self.server = server.Server(controller=self)

    def run(self):

        while not self.shutdown.is_set():
            self.log("Waiting for a message.")
            message = self.queue.get()
            self.handle_message(message)

        self.log("I'm dead.")

    def close_program(self):

        self.log("Close program.")

        # For aborting launching of the (properly speaking)
        # server if it was not launched
        self.server.shutdown()
        self.shutdown.set()

    def ask_interface(self, instruction, arg=None):

        self.mod.ask_interface(instruction, arg)

    # ------------------------------- Message handling ----------------------------------------------- #

    def handle_message(self, message):

        command = message[0]
        args = message[1]

        func = getattr(self, command)

        if args is not None:
            func(*args)

        else:
            func()

        self.log("Message handled.")

    # ------------------------------ Server interface ---------------------------------------- #

    def stop_server(self):

        self.log("Stop server.")
        self.server.shutdown()

    def start_server(self):
        self.server.run()

    def server_error(self, error_message):

        self.log("Server error.")
        self.ask_interface("server_error", error_message)

    # -------------------- Parameters management ---------------------------------------------- #

    def get_parameters(self, key):

        return self.data.param[key]

    # --------------------- UI interface ------------------------------------------------------- #

    def ui_ready(self):

        self.log("UI is ready.")

    def ui_close_window(self):

        self.log("UI close window.")
        self.close_program()
