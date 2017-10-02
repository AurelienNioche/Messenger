import sys
from PyQt5.QtWidgets import QApplication

from . import interface, controller


class Model:
    """Model class.
    Create the elements of the model, orchestrate their interactions.
    """

    def __init__(self):

        self.app = QApplication(sys.argv)
        self.ui = interface.UI(model=self)
        self.controller = controller.Controller(model=self)

    def run(self):

        try:

            self.controller.start()
            self.ui.setup()
            sys.exit(self.app.exec_())

        except Exception as e:
            self.ui.fatal_error(error_message=str(e))

    def ask_interface(self, instruction, arg=None):

        self.ui.queue.put((instruction, arg))
        self.ui.communicate.signal.emit()

    def ask_controller(self, instruction, arg=None):

        self.controller.queue.put((instruction, arg))
