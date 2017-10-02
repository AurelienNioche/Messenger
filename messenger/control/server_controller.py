from multiprocessing import Queue, Event
from threading import Thread

from utils.logger import Logger
from . control import data,  server


class MVCController(Thread, Logger):
    name = "Controller"

    def __init__(self, model):

        super().__init__()

        self.mod = model

        # For receiving inputs
        self.queue = Queue()

        self.running_game = Event()
        self.running_server = Event()

        self.shutdown = Event()
        self.fatal_error = Event()
        self.continue_game = Event()
        self.device_scanning_event = Event()

        self.data = data.Data(controller=self)
        self.server = server.Server(controller=self)

    def run(self):

        self.log("Waiting for a message.")
        go_signal_from_ui = self.queue.get()
        self.log("Got go signal from UI: '{}'.".format(go_signal_from_ui))

        while not self.shutdown.is_set():
            self.log("Waiting for a message.")
            message = self.queue.get()
            self.handle_message(message)

        self.close_program()

    def close_program(self):

        self.log("Close program.")

        # For aborting launching of the (properly speaking)
        # server if it was not launched
        self.server.queue.put(("Abort",))
        self.server.shutdown()
        self.server.end()
        self.shutdown.set()

    def stop_server(self):

        self.log("Stop server.")
        self.server.shutdown()

    def start_server(self):

        if not self.running_server.is_set():
            self.server.start()

        self.server.queue.put(("Go",))

    def server_running(self):

        self.log("Server running.")
        self.running_server.set()

    def server_error(self, error_message):

        self.log("Server error.")
        self.ask_interface("server_error", error_message)

    def get_parameters(self, key):

        return self.data.param[key]
