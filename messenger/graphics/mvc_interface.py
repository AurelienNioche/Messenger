from multiprocessing import Queue, Event
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, Qt, QSettings
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QDesktopWidget

from messenger.graphics import message_box
from utils.logger import Logger


class Communicate(QObject):
    signal = pyqtSignal()


class MVCInterface(message_box.MessageBoxApplication, Logger):

    name = "Interface"
    app_name = "MVCInterface"

    # noinspection PyArgumentList
    def __init__(self, model):

        super().__init__()

        self.model = model

        self.occupied = Event()
        self.queue = Queue()
        self.communicate = Communicate()
        self.settings = QSettings("HumanoidVsAndroid", self.app_name)

    @property
    def dimensions(self):

        desktop = QDesktopWidget()
        dimensions = desktop.screenGeometry()  # get screen geometry
        w = dimensions.width() * 0.5  # 50% of the screen width
        h = dimensions.height() * 0.5  # 50% of the screen height

        return 300, 100, w, h

    def setup(self):

        # For communication with model
        self.communicate.signal.connect(self.look_for_msg)

        # Retrieve geometry
        self.setup_geometry()

        # Name the window
        self.setWindowTitle(self.app_name)

        # Tell the model ui is ready
        self.ask_controller("ui_ready")

        self.show()

    def setup_geometry(self):

        # Retrieve geometry
        self.setGeometry(*self.dimensions)
        try:
            self.restoreGeometry(self.settings.value("geometry"))

        except Exception as e:
            self.log(str(e))

    def closeEvent(self, event):

        if self.isVisible() and self.show_question("Are you sure you want to quit?"):

            self.before_closing()
            event.accept()

        else:
            self.log("Ignore close window.")
            event.ignore()

    def before_closing(self):

        self.save_geometry()
        self.ask_controller("ui_close_window")
        self.log("Close window.")

    def save_geometry(self):

        self.settings.setValue("geometry", self.saveGeometry())

    def fatal_error(self, error_message):

        self.show_critical(msg="Fatal error.\nError message: '{}'.".format(error_message))
        self.before_closing()
        self.close()

    # ---------------------- Communication ------------------ #

    def look_for_msg(self):

        if not self.occupied.is_set():
            self.occupied.set()

            msg = self.queue.get()
            self.handle_message(msg)

            # Able now to handle a new display instruction
            self.occupied.clear()

        else:
            # noinspection PyCallByClass, PyTypeChecker
            QTimer.singleShot(100, self.look_for_msg)

    def handle_message(self, message):

        command = message[0]
        args = message[1]

        func = getattr(self, command)

        if args is not None:
            func(*args)

        else:
            func()

    def ask_controller(self, instruction, arg=None):

        self.model.ask_controller(instruction, arg)
