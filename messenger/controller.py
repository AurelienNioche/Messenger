from messenger.control import mvc_controller


class Controller(mvc_controller.MVCController):
    name = "Controller"

    def __init__(self, model):

        super().__init__(model=model)
