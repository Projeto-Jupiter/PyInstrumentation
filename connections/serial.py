import time

from connections import ConnectionHandler, NoDataAvailableException


class SerialHandler(ConnectionHandler):

    def __init__(self, baudrate, serialport, module):
        super().__init__()
        self.baudrate = baudrate
        self.serialport = serialport
        self.ser = None
        self.serial_module = module
        self.connect()

    def connect(self):
        self.ser = self.serial_module()
        self.ser.baudrate = self.baudrate
        self.ser.port = self.serialport
        self.ser.open()
        self.flush_buffer()

    def flush_buffer(self):
        # testar
        self.ser.flushInput()
        self.ser.flushOutput()

    def reset(self):
        self.ser.close()
        time.sleep(2)
        self.connect()

    def fetch_data(self):
        try:
            data = self.ser.readline()
        except Exception:
            raise NoDataAvailableException()
        return data

    def write(self, msg):
        self.ser.write(msg)
