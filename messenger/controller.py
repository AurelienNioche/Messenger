from messenger.control import mvc_controller


class Controller(mvc_controller.MVCController):
    name = "Controller"

    def __init__(self, model):

        super().__init__(model=model)

    def ui_new_message(self, user_name, message):

        self.log("Got new message from ui for {}: '{}'.".format(user_name, message))
        self.server.send_message(user_name, message)

    def ui_ready(self):

        super().ui_ready()
        self.server.start()
