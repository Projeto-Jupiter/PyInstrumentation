from connections.serial import SerialHandler
from connections.telnet import TelnetHandler
from constants import BAUD_RATE, MOCK, SERIAL_PORT, IP, SP


if __name__ == "__main__":
    if MOCK:
        from connections.mocks.SerialMock import Serial
        from connections.mocks.TelnetMock import Telnet
    else:
        from serial import Serial
        from telnetlib import Telnet

    #connection = SerialHandler(BAUD_RATE, SERIAL_PORT, Serial)
    connection = TelnetHandler(IP, SERIAL_PORT, Telnet)
    from widget import Application
    widget_app = Application(connection)
