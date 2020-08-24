import os

from connections import NoDataAvailableException


class Telnet:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'static.csv')
        self._data = open(path).read()

    def write(self, msg):
        print(msg)
        return

    def flushInput(self):
        pass

    def flushOutput(self):
        pass

    def read_all(self):
        pass

    def read_until(self, expected_output):
        try:
            returnIndex = self._data.index(expected_output)
        except ValueError:
            raise NoDataAvailableException()

        if returnIndex != -1:
            s = self._data[0:returnIndex + 1]
            self._data = self._data[returnIndex + 1:]
            return s
        else:
            return ""
