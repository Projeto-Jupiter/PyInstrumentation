import time

from Serial import serial
from mocks.SerialMock import Serial


class SerialConnection:

    def __init__(self, baudrate, serialport, mock=True):
        self.baudrate = baudrate
        self.serialport = serialport
        self.mock = mock
        self.ser = None
        self.connectSerial()

    def connectSerial(self):
        if self.mock:
            self.ser = Serial()
        else:
            self.ser = serial.Serial()
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
        self.connectSerial()
