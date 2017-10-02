from . graphics import mvc_interface, git_app, main_frame


class UI(mvc_interface.MVCInterface, git_app.GitApplication, main_frame.MainFrame):

    app_name = "Messenger"

    def __init__(self, model):

        super().__init__(model=model)
