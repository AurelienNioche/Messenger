from PyQt5 import QtCore, QtWidgets


class LeftPanel(QtWidgets.QWidget):

    def __init__(self):

        QtWidgets.QWidget.__init__(self)

        layout = QtWidgets.QVBoxLayout()

        self.conversation_picker = ConversationPicker()

        layout.addWidget(self.conversation_picker)

        self.setLayout(layout)


class RightPanel(QtWidgets.QWidget):

    def __init__(self):

        QtWidgets.QWidget.__init__(self)

        layout = QtWidgets.QVBoxLayout()

        self.conversation_content = ConversationContent()
        self.message_writer = MessageWriter()

        layout.addWidget(self.conversation_content)
        layout.addWidget(self.message_writer)

        self.setLayout(layout)


class MessageWriter(QtWidgets.QWidget):

    def __init__(self):

        QtWidgets.QWidget.__init__(self)

        layout = QtWidgets.QHBoxLayout()

        message_content = QtWidgets.QPlainTextEdit("Here takes place the content of message.")

        button_send = QtWidgets.QPushButton("Send")
        button_send.clicked.connect(self.send)

        layout.addWidget(message_content)
        layout.addWidget(button_send)

        self.setLayout(layout)

    def send(self):

        pass


class ConversationContent(QtWidgets.QWidget):

    def __init__(self):

        QtWidgets.QWidget.__init__(self)

        layout = QtWidgets.QHBoxLayout()

        message_content = QtWidgets.QLabel("Here takes place the content of the conversation.")

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(message_content)

        layout.addWidget(scroll_area)

        self.setLayout(layout)


class ConversationPicker(QtWidgets.QWidget):

    def __init__(self):

        QtWidgets.QWidget.__init__(self)

        group = QtWidgets.QWidget(self)

        self.button_new_conversation = QtWidgets.QPushButton("New")
        self.button_new_conversation.clicked.connect(self.new_conversation)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.horizontalScrollBar().setEnabled(False)

        button_layout = QtWidgets.QVBoxLayout(group)

        button_layout.addWidget(self.button_new_conversation)
        for i in range(30):
            button_layout.insertWidget(0, QtWidgets.QPushButton("Conversation{}".format(i)))

        group.setLayout(button_layout)
        scroll_area.setWidget(group)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def new_conversation(self):

        pass


class Window(QtWidgets.QWidget):

    def __init__(self):

        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout(self)

        left_panel = LeftPanel()
        right_panel = RightPanel()

        layout.addWidget(left_panel, alignment=QtCore.Qt.AlignHCenter)
        layout.addWidget(right_panel)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.resize(1000, 500)
    window.show()
    sys.exit(app.exec_())