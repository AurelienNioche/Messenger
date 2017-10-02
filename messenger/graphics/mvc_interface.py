from multiprocessing import Queue, Event
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, Qt, QSettings
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QDesktopWidget

from utils.logger import Logger


class Communicate(QObject):
    signal = pyqtSignal()


class MVCInterface(QWidget, Logger):
    name = "Interface"
    app_name = "MVCInterface"

    # noinspection PyArgumentList
    def __init__(self, model):

        super().__init__()

        self.mod = model

        self.occupied = Event()
        self.queue = Queue()
        self.communicate = Communicate()
        self.settings = QSettings("HumanoidVsAndroid", self.app_name)

        self.frames = dict()

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

    def setup_geometry(self):

        # Retrieve geometry
        self.setGeometry(*self.dimensions)
        try:
            self.restoreGeometry(self.settings.value("geometry"))

        except Exception as e:
            self.log(str(e))

    def setup_widgets(self):

        layout = QVBoxLayout()

        grid = QGridLayout()

        for frame in self.frames.values():
            # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
            grid.addWidget(frame, 0, 0)

        grid.setAlignment(Qt.AlignCenter)
        layout.addLayout(grid, stretch=1)

        self.setLayout(layout)

    def closeEvent(self, event):

        if self.isVisible() and self.show_question("Are you sure you want to quit?"):

            self.save_geometry()
            self.log("Close window")
            self.close_window()
            event.accept()

        else:
            self.log("Ignore close window.")
            event.ignore()

    def save_geometry(self):

        self.settings.setValue("geometry", self.saveGeometry())

    def show_frame(self, name):

        for frame in self.frames.values():
            frame.hide()

        self.frames[name].show()

    def fatal_error(self, error_message):

        self.show_critical(msg="Fatal error.\nError message: '{}'.".format(error_message))
        self.close_window()
        self.close()

    def look_for_msg(self):

        if not self.occupied.is_set():
            self.occupied.set()

            msg = self.queue.get()
            self.log("I received message '{}'.".format(msg))

            command = eval("self.{}".format(msg[0]))
            args = msg[1:]
            if args:
                command(*args)
            else:
                command()

            # Able now to handle a new display instruction
            self.occupied.clear()

        else:
            # noinspection PyCallByClass, PyTypeChecker
            QTimer.singleShot(100, self.look_for_msg)

    def ask_controller(self, instruction, arg=None):
        self.model.ask_controller(instruction, arg)
