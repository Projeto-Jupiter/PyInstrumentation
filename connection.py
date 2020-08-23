import time


class NoDataAvailableException(Exception):
    """Exception to be raised when there isn't any data available for retrieval"""
    pass


class SerialHandler:

    def __init__(self, baudrate, serialport, serial_module):
        self.baudrate = baudrate
        self.serialport = serialport
        self.ser = None
        self.serial_module = serial_module
        self.connect_serial()

    def connect_serial(self):
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
        self.connect_serial()

    def fetch_data(self):
        try:
            data = self.ser.readline()
        except Exception:
            raise NoDataAvailableException()
        return data
