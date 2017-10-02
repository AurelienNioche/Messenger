from multiprocessing import Queue, Event
from subprocess import getoutput

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, Qt, QSettings
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QDesktopWidget

from .graphics import *
from utils.logger import Logger


class Communicate(QObject):
    signal = pyqtSignal()


class UI(QWidget, Logger):
    name = "Interface"
    app_name = "Messenger"

    # noinspection PyArgumentList
    def __init__(self, model):

        super().__init__()

        self.mod = model

        self.occupied = Event()

        self.layout = QVBoxLayout()

        self.frames = dict()

        # refresh interface and update data (tables, figures)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)

        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

        self.already_asked_for_saving_parameters = 0

        self.queue = Queue()

        self.communicate = Communicate()

        self.settings = QSettings("HumanoidVsAndroid", "Duopoly")

        self.controller_queue = None

    @property
    def dimensions(self):

        desktop = QDesktopWidget()
        dimensions = desktop.screenGeometry()  # get screen geometry
        w = dimensions.width() * 0.9  # 90% of the screen width
        h = dimensions.height() * 0.8  # 80% of the screen height

        return 300, 100, w, h

    def setup(self):

        self.check_update()

        self.controller_queue = self.mod.controller.queue

        # self.frames["devices"] = \
        #     devices_view.DevicesFrame(parent=self)

        self.setWindowTitle(self.app_name)

        self.communicate.signal.connect(self.look_for_msg)

        self.setGeometry(*self.dimensions)

        grid = QGridLayout()

        for frame in self.frames.values():
            # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
            grid.addWidget(frame, 0, 0)

        grid.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(grid, stretch=1)

        self.setLayout(self.layout)

        # get saved geometry
        try:
            self.restoreGeometry(self.settings.value("geometry"))

        except Exception as e:
            self.log(str(e))

        self.send_go_signal()

    def check_update(self):

        self.log("I check for updates.")
        getoutput("git fetch")
        git_msg = getoutput("git diff origin/master")
        self.log("Git message is: '{}'".format(git_msg))

        if git_msg:

            if self.show_question(
                    "An update is available.",
                    question="Do you want to update now?", yes="Yes", no="No", focus="Yes"):

                git_output = getoutput("git pull")
                self.log("User wants to update. Git message is: {}".format(git_output))
                success = 0

                if "Updating" in git_output:
                    success = 1

                else:
                    for msg in ["git stash", "git pull", "git stash pop"]:
                        git_output = getoutput(msg)
                        self.log("Command is '{}' Git message is: '{}'".format(msg, git_output))

                    if "Updating" in git_output:
                        success = 1

                if success:
                    self.show_info("Updated successfully. Modifications will be effective at the next restart.")

                else:
                    self.show_warning("An error occurred. No modifications have been done.")

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

    def ask_controller(self, controller_function, arg=None):
        self.controller_queue.put((controller_function, arg))
