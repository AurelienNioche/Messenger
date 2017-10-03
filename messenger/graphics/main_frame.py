from PyQt5 import QtCore, QtWidgets
import sys


class Conversations:

    def __init__(self, parent):

        self.dic = {}

        self.selected = None
        self.parent = parent

    def create_new_conversation(self, user_name):

        self.dic[user_name] = Conversation(user_name)

    def change_selected(self, user_name):

        self.selected = user_name

    def new_message_from_admin(self, message):

        if self.selected is not None and message:

            self.add_content(user_name=self.selected, emitter="Admin", content=message)

    def new_message_from_user(self, user_name, message):

        self.add_content(user_name, user_name, message)

    def get_current_content(self):

        return self.dic[self.selected].content

    def add_content(self, user_name, emitter, content):

        self.dic[user_name].add_content("[{}] {}\n".format(emitter, content))


class Conversation:

    def __init__(self, user_name):

        super().__init__()

        self.user_name = user_name
        self.content = ""

    def add_content(self, new_content):

        self.content += new_content


class LeftPanel(QtWidgets.QWidget):

    def __init__(self, parent, conversation_picker):
        # noinspection PyArgumentList
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.conversation_picker = conversation_picker

        layout = QtWidgets.QVBoxLayout(self)

        button_new_conversation = QtWidgets.QPushButton("New")
        # noinspection PyUnresolvedReferences
        button_new_conversation.clicked.connect(self.click_new_conversation)

        # noinspection PyArgumentList
        layout.addWidget(self.conversation_picker)
        # noinspection PyArgumentList
        layout.addWidget(button_new_conversation)

    def click_new_conversation(self):

        # noinspection PyArgumentList
        user_name, ok = QtWidgets.QInputDialog().getText(self, 'New conversation', 'To:')

        if ok:

            self.parent().change_selected_conversation(user_name)
            return True

        else:
            return False

class RightPanel(QtWidgets.QWidget):

    def __init__(self, parent, message_writer, conversation_display):
        # noinspection PyArgumentList
        QtWidgets.QWidget.__init__(self, parent=parent)

        layout = QtWidgets.QVBoxLayout()

        self.conversation_display_support = \
            ConversationDisplaySupport(parent=parent, conversation_display=conversation_display)
        self.message_writer = message_writer

        # noinspection PyArgumentList
        layout.addWidget(self.conversation_display_support)
        # noinspection PyArgumentList
        layout.addWidget(self.message_writer)

        self.setLayout(layout)


class MessageWriter(QtWidgets.QWidget):

    def __init__(self, interface):

        # noinspection PyArgumentList
        QtWidgets.QWidget.__init__(self)

        self.interface = interface

        layout = QtWidgets.QHBoxLayout(self)

        self.message_content = QtWidgets.QPlainTextEdit()

        button_send = QtWidgets.QPushButton("Send")
        # noinspection PyUnresolvedReferences
        button_send.clicked.connect(self.send)
        button_send.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # noinspection PyArgumentList
        layout.addWidget(self.message_content)
        # noinspection PyArgumentList
        layout.addWidget(button_send)

    def send(self):

        self.interface.new_message_from_admin(self.message_content.toPlainText())
        self.message_content.setPlainText("")

    def keyReleaseEvent(self, e):

        if e.key() == QtCore.Qt.Key_Return:

            self.interface.new_message_from_admin(self.message_content.toPlainText()[:-2])
            self.message_content.setPlainText("")


class ConversationDisplaySupport(QtWidgets.QWidget):

    def __init__(self, parent, conversation_display):

        # noinspection PyArgumentList
        QtWidgets.QWidget.__init__(self, parent=parent)

        layout = QtWidgets.QHBoxLayout(self)
        # noinspection PyArgumentList
        layout.addWidget(conversation_display)


class ConversationPicker(QtWidgets.QTableWidget):

    def __init__(self, interface):

        super().__init__(0, 1)

        self.interface = interface

        self.verticalHeader().hide()
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().hide()

        # noinspection PyUnresolvedReferences
        self.clicked.connect(self.click_on_case)

        self.list = []

    def create_new_entry(self, user_name):

        self.insertRow(0)
        self.setItem(0, 0, QtWidgets.QTableWidgetItem(user_name))
        self.list.append(user_name)
        self.selectRow(0)

    def click_on_case(self, row_index):

        user_name = self.list[-(1 + row_index.row())]
        self.interface.change_selected_conversation(user_name)


class ConversationDisplay(QtWidgets.QPlainTextEdit):

    def __init__(self):

        super().__init__()

        self.setReadOnly(True)

    def display(self, text):

        self.setPlainText(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class MainFrame(QtWidgets.QWidget):

    def __init__(self):

        # noinspection PyArgumentList
        super().__init__()

        layout = QtWidgets.QHBoxLayout(self)

        self.conversation_display = ConversationDisplay()
        self.conversations = Conversations(parent=self)

        self.conversation_picker = ConversationPicker(interface=self)
        self.message_writer = MessageWriter(interface=self)

        self.left_panel = \
            LeftPanel(parent=self, conversation_picker=self.conversation_picker)
        self.right_panel = \
            RightPanel(parent=self, message_writer=self.message_writer, conversation_display=self.conversation_display)

        layout.addWidget(self.left_panel, alignment=QtCore.Qt.AlignHCenter)
        # noinspection PyArgumentList
        layout.addWidget(self.right_panel)

    def change_selected_conversation(self, user_name):

        # Because SQL is case insensitive
        user_name = user_name.lower().capitalize()

        if user_name not in self.conversations.dic.keys():
            self.conversations.create_new_conversation(user_name)
            self.conversation_picker.create_new_entry(user_name)

        self.conversations.change_selected(user_name)
        content = self.conversations.get_current_content()

        self.conversation_display.display(content)

    def new_message_from_admin(self, message):

        if self.conversations.selected is None:
            if self.left_panel.click_new_conversation():
                pass
            else:
                return

        self.conversations.new_message_from_admin(message)
        self.conversation_display.display(self.conversations.get_current_content())
        self.ask_controller("ui_new_message", (self.conversations.selected, message))

    def new_message_from_user(self, user_name, message):

        # Because SQL is case insensitive
        user_name = user_name.lower().capitalize()

        if user_name not in self.conversations.dic.keys():
            self.conversations.create_new_conversation(user_name)
            self.conversation_picker.create_new_entry(user_name)

        self.conversations.new_message_from_user(user_name, message)

        if self.conversations.selected is None:
            self.conversations.selected = user_name

        if self.conversations.selected == user_name:
            self.conversation_display.display(self.conversations.get_current_content())


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MainFrame()
    window.resize(1000, 500)
    window.show()
    sys.exit(app.exec_())
