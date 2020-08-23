from constants import BAUD_RATE, MOCK, SERIAL_PORT
from connection import SerialHandler

if __name__ == "__main__":
    if MOCK:
        from mocks.SerialMock import Serial
    else:
        from serial import Serial

    connection = SerialHandler(BAUD_RATE, SERIAL_PORT, Serial)
    from widget import Application
    widget_app = Application(connection)
