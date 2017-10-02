from PyQt5 import QtCore, QtWidgets
import sys


class Conversations:

    def __init__(self, parent, conversation_display):

        self.conversation_display = conversation_display
        self.dic = {}

        self.selected = None
        self.parent = parent

    def create_new_conversation(self, user_name):

        self.dic[user_name] = Conversation(user_name)

    def change_selected(self, user_name):

        self.selected = user_name

        content = self.dic[user_name].content

        if content:
            self.conversation_display.display(content)
        else:
            self.conversation_display.display(
                "Content of conversation with '{}' will appear here...\n".format(user_name))

    def new_message(self, who, what):

        if self.selected is not None and what:

            self.dic[self.selected].add_content("[{}] {}\n".format(who, what))
            self.conversation_display.display(self.dic[self.selected].content)
            self.parent.ask_controller("ui_new_message", (self.selected, what))


class Conversation:

    def __init__(self, user_name):

        super().__init__()

        self.user_name = user_name
        self.content = ""

    def add_content(self, new_content):

        self.content += new_content


class LeftPanel(QtWidgets.QWidget):

    def __init__(self, parent, conversations):

        QtWidgets.QWidget.__init__(self, parent=parent)

        self.conversations = conversations

        layout = QtWidgets.QVBoxLayout(self)

        button_new_conversation = QtWidgets.QPushButton("New")
        button_new_conversation.clicked.connect(self.ask_for_new_conversation)

        self.conversation_picker = ConversationPicker(parent=self, conversations=conversations)

        layout.addWidget(self.conversation_picker)
        layout.addWidget(button_new_conversation)

    def ask_for_new_conversation(self):

        user_name, ok = QtWidgets.QInputDialog.getText(self, 'New conversation', 'To:')

        if ok and user_name not in self.conversations.dic.keys():

            self.conversation_picker.create_new_conversation(user_name)


class RightPanel(QtWidgets.QWidget):

    def __init__(self, parent, conversations, conversation_display):

        QtWidgets.QWidget.__init__(self, parent=parent)

        layout = QtWidgets.QVBoxLayout()

        self.conversation_display_support = \
            ConversationDisplaySupport(parent=parent, conversation_display=conversation_display)
        self.message_writer = MessageWriter(parent=self, conversations=conversations)

        layout.addWidget(self.conversation_display_support)
        layout.addWidget(self.message_writer)

        self.setLayout(layout)


class MessageWriter(QtWidgets.QWidget):

    def __init__(self, parent, conversations):

        QtWidgets.QWidget.__init__(self, parent=parent)

        self.conversations = conversations

        layout = QtWidgets.QHBoxLayout(self)

        self.message_content = QtWidgets.QPlainTextEdit("Here takes place the content of message.")

        button_send = QtWidgets.QPushButton("Send")
        button_send.clicked.connect(self.send)

        layout.addWidget(self.message_content)
        layout.addWidget(button_send)

    def send(self):

        self.conversations.new_message("Admin", self.message_content.toPlainText())
        self.message_content.setPlainText("")


class ConversationDisplaySupport(QtWidgets.QWidget):

    def __init__(self, parent, conversation_display):

        QtWidgets.QWidget.__init__(self, parent=parent)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(conversation_display)


class ConversationPicker(QtWidgets.QTableWidget):

    def __init__(self, parent, conversations):

        super().__init__(0, 1, parent)

        self.conversations = conversations

        self.verticalHeader().hide()
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().hide()

        self.clicked.connect(self.click_on_case)

        self.list = []

    def create_new_conversation(self, user_name):

        self.insertRow(0)
        self.setItem(0, 0, QtWidgets.QTableWidgetItem(user_name))
        self.list.append(user_name)
        self.selectRow(0)

        self.conversations.create_new_conversation(user_name)
        self.conversations.change_selected(user_name)

    def click_on_case(self, row_index):

        user_name = self.list[-(1 + row_index.row())]
        self.conversations.change_selected(user_name)


class ConversationDisplay(QtWidgets.QPlainTextEdit):

    def __init__(self):

        super().__init__()

        self.setReadOnly(True)
        self.display("Here takes place the content of the conversation.")

    def display(self, text):

        self.setPlainText(text)

        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class MainFrame(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        layout = QtWidgets.QHBoxLayout(self)

        self.conversation_display = ConversationDisplay()
        self.conversations = Conversations(parent=self, conversation_display=self.conversation_display)

        self.left_panel = \
            LeftPanel(parent=self, conversations=self.conversations)
        self.right_panel = \
            RightPanel(parent=self, conversations=self.conversations, conversation_display=self.conversation_display)

        layout.addWidget(self.left_panel, alignment=QtCore.Qt.AlignHCenter)
        layout.addWidget(self.right_panel)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MainFrame()
    window.resize(1000, 500)
    window.show()
    sys.exit(app.exec_())
