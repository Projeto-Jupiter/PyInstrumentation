from connections.network import NetworkConfigurator
from connections.serial import SerialHandler
from connections.telnet import TelnetHandler
from constants import MOCK

import json
import os

if __name__ == "__main__":
    if MOCK:
        from connections.mocks.SerialMock import Serial
        from connections.mocks.TelnetMock import Telnet
    else:
        from serial import Serial
        from telnetlib import Telnet

    config_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configurations.json')
    raw_data = open(config_data_path).read()
    config_data = json.loads(raw_data)
    connection = NetworkConfigurator(config_data, Telnet, TelnetHandler)
    from widget import Application

    widget_app = Application(connection)
