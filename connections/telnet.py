import time

from connections import ConnectionHandler, NoDataAvailableException


class TelnetHandler(ConnectionHandler):

    def __init__(self, ip, port, module):
        super().__init__()
        self.ip = ip
        self.port = port
        self.telnet_module = module
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = self.telnet_module(self.ip, self.port)
        self.flush_buffer()

    def flush_buffer(self):
        # testar
        self.connection.read_all()

    def reset(self):
        self.connection.close()
        time.sleep(2)
        self.connect()

    def fetch_data(self, expected_output="\n"):
        try:
            data = self.connection.read_until(expected_output)
        except Exception:
            raise NoDataAvailableException()
        return data

    def write(self, msg):
        self.connection.write(msg)
