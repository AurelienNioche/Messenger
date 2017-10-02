from PyQt5 import QtWidgets


class MessageBoxApplication(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

    def show_question(self, msg, question="", yes="Yes", no="No", focus="No"):
        """question with customs buttons"""

        msgbox = QtWidgets.QMessageBox(self)
        msgbox.setText(msg)
        msgbox.setInformativeText(question)
        msgbox.setIcon(QtWidgets.QMessageBox.Question)
        no_button = msgbox.addButton(no, QtWidgets.QMessageBox.ActionRole)
        yes_button = msgbox.addButton(yes, QtWidgets.QMessageBox.ActionRole)
        msgbox.setDefaultButton((no_button, yes_button)[focus == no])

        msgbox.exec_()

        return msgbox.clickedButton() == yes_button

    def show_warning(self, msg):
        button_reply = QtWidgets.QMessageBox().warning(
            self, "", msg,
            QtWidgets.QMessageBox.Ok
        )

        return button_reply == QtWidgets.QMessageBox.Yes

    def show_critical_and_retry(self, msg):
        button_reply = QtWidgets.QMessageBox().critical(
            self, "", msg,  # Parent, title, message
            QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Retry,  # Buttons
            QtWidgets.QMessageBox.Retry  # Default button
        )

        return button_reply == QtWidgets.QMessageBox.Retry

    def show_critical_and_ok(self, msg):
        button_reply = QtWidgets.QMessageBox().critical(
            self, "", msg,  # Parent, title, message
            QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Ok,  # Buttons
            QtWidgets.QMessageBox.Ok  # Default button
        )

        return button_reply == QtWidgets.QMessageBox.Ok

    def show_critical(self, msg):
        QtWidgets.QMessageBox().critical(
            self, "", msg,  # Parent, title, message
            QtWidgets.QMessageBox.Close
        )

    def show_info(self, msg):
        QtWidgets.QMessageBox().information(
            self, "", msg,
            QMessageBox.Ok
        )