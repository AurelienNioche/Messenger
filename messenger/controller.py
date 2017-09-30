from multiprocessing import Queue, Event
from threading import Thread

from utils.logger import Logger
from . control import data,  server


class Controller(Thread, Logger):
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

        # For giving instructions to graphic process
        self.graphic_queue = self.mod.ui.queue
        self.communicate = self.mod.ui.communicate

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

    def ask_interface(self, instruction, arg=None):

        if arg is not None:
            self.graphic_queue.put((instruction, arg))
        else:
            self.graphic_queue.put((instruction,))
        self.communicate.signal.emit()

    def stop_server(self):

        self.log("Stop server.")
        self.server.shutdown()

    def start_server(self):

        if not self.running_server.is_set():
            self.server.start()

        self.server.queue.put(("Go",))

    # ------------------------------- Message handling ----------------------------------------------- #

    def handle_message(self, message):

        command = message[0]
        args = message[1:]
        if len(args):
            eval("self.{}(*args)".format(command))
        else:
            eval("self.{}()".format(command))

    # ------------------------------ Server interface ----------------------------------------#

    def server_running(self):

        self.log("Server running.")
        self.running_server.set()

    def server_error(self, error_message):

        self.log("Server error.")
        self.ask_interface("server_error", error_message)

    def get_parameters(self, key):

        return self.data.param[key]
