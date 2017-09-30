from multiprocessing import Queue, Event
from threading import Thread
from urllib import parse, request

from utils.logger import Logger


class Server(Thread, Logger):
    name = "Server"

    def __init__(self, controller):

        Thread.__init__(self)

        self.cont = controller
        self.param = self.cont.get_parameters("network")

        self.queue = Queue()

        self.shutdown_event = Event()
        self.wait_event = Event()

        self.server_address = self.param["website"] + "messenger.php"

    def run(self):

        while not self.shutdown_event.is_set():

            self.log("Waiting for a message...")
            msg = self.queue.get()
            self.log("I received msg '{}'.".format(msg))

            if msg and msg[0] == "Go":
                self.wait_event.clear()
                self.serve()

        self.log("I'm dead.")

    def send_request(self, **kwargs):

        assert "demandType" in kwargs and "userName" in kwargs and "message" in kwargs, \
            "A request to the server should contains a 'demandType', a 'userName' and a 'message'."

        print("I will use the url: '{}'.".format(self.server_address))

        data = parse.urlencode(kwargs).encode()

        req = request.Request(self.server_address, data=data)
        enc_resp = request.urlopen(req)

        response = enc_resp.read().decode()

        print("I called the page '{}' with a post request (args: '{}').".format(self.server_address, data))
        print("I received the response: '{}'.".format(response))

        return response

    def serve(self):

        while not self.wait_event.is_set():

            try:

                print("I send a request for receiving the messages intended to server.")

                response = self.send_request(
                    demandType="serverHears",
                    userName="none",
                    message="none"
                )

                if "reply" in response:
                    args = [i for i in response.split("/") if i]
                    n_messages = int(args[1])

                    print("I received {} new message(s).".format(n_messages))

                    if n_messages:
                        for arg in args[2:]:
                            sep_args = arg.split("<>")

                            user_name, message = sep_args[0], sep_args[1]

                            print("I send confirmation for message '{}'.".format(arg))
                            self.send_request(
                                demandType="serverReceiptConfirmation",
                                userName=user_name,
                                message=message
                            )

            except Exception as e:
                self.log("Got error '{}'.".format(e))

    def shutdown(self):
        self.wait_event.set()

    def end(self):
        self.shutdown_event.set()
        self.queue.put("break")

    def send_message(self, user_name, message):

        print("I send a request for sending a message as the server.")

        self.send_request(
            demandType="serverSpeaks",
            userName=user_name,
            message=message
        )

    def empty_tables(self):

        print("I send a request for erasing tables.")

        self.send_request(
            demandType="emptyTables",
            userName="none",
            message="none"
        )

