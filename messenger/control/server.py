from multiprocessing import Event
from threading import Thread
from urllib import parse, request

from utils.logger import Logger


class Server(Thread, Logger):
    name = "Server"
    time_between_requests = 1

    def __init__(self, controller):

        Thread.__init__(self)

        self.cont = controller
        self.param = self.cont.get_parameters("network")

        self.shutdown_event = Event()
        self.waiting_event = Event()

        self.server_address = self.param["website"] + "/messenger.php"

    def run(self):

        while not self.shutdown_event.is_set():

            self.receive_messages()
            self.waiting_event.wait(self.time_between_requests)

        self.log("I'm dead.")

    def shutdown(self):

        self.waiting_event.set()
        self.shutdown_event.set()

    def send_request(self, **kwargs):

        assert "demandType" in kwargs and "userName" in kwargs and "message" in kwargs, \
            "A request to the server should contains a 'demandType', a 'userName' and a 'message'."

        self.log("I will use the url: '{}'.".format(self.server_address))

        data = parse.urlencode(kwargs).encode()

        req = request.Request(self.server_address, data=data)
        enc_resp = request.urlopen(req)

        response = enc_resp.read().decode()

        self.log("I called the page '{}' with a post request (args: '{}').".format(self.server_address, data))
        self.log("I received the response: '{}'.".format(response))

        return response

    def receive_messages(self):

        self.log("I send a request for receiving the messages intended to server.")

        response = self.send_request(
            demandType="serverHears",
            userName="none",
            message="none"
        )

        if "reply" in response:
            args = [i for i in response.split("/") if i]
            n_messages = int(args[1])

            self.log("I received {} new message(s).".format(n_messages))

            if n_messages:
                for arg in args[2:]:
                    sep_args = arg.split("<>")

                    user_name, message = sep_args[0], sep_args[1]

                    self.log("I send confirmation for message '{}'.".format(arg))
                    self.send_request(
                        demandType="serverReceiptConfirmation",
                        userName=user_name,
                        message=message
                    )

    def send_message(self, user_name, message):

        self.log("I send a request for sending a message as the server.")

        self.send_request(
            demandType="serverSpeaks",
            userName=user_name,
            message=message
        )

    def empty_tables(self):

        self.log("I send a request for erasing tables.")

        self.send_request(
            demandType="emptyTables",
            userName="none",
            message="none"
        )

