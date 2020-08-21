import os


class NoDataAvailableException(Exception):
    """Exception to be raised when there isn't any data available for retrieval"""
    pass


# a Serial class emulator
class Serial:

    ## init(): the constructor.  Many of the arguments have default values
    # and can be skipped when calling the constructor.
    def __init__(self, port='COM1', baudrate=19200, timeout=1,
                 bytesize=8, parity='N', stopbits=1, xonxoff=0,
                 rtscts=0):
        self.name = port
        self.port = port
        self.timeout = timeout
        self.parity = parity
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self._isOpen = True
        self._receivedData = ""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'static.csv')
        self._data = open(path).read()

    ## isOpen()
    # returns True if the port to the Arduino is open.  False otherwise
    def isOpen(self):
        return self._isOpen

    ## open()
    # opens the port
    def open(self):
        self._isOpen = True

    ## close()
    # closes the port
    def close(self):
        self._isOpen = False

    ## write()
    # writes a string of characters to the Arduino
    def write(self, string):
        print('Arduino got: "' + string + '"')
        self._receivedData += string

    ## read()
    # reads n characters from the fake Arduino. Actually n characters
    # are read from the string _data and returned to the caller.
    def read(self, n=1):
        # s = self._data[0:n]
        # self._data = self._data[n:]
        # print( "read: now self._data = ", self._data )
        # return s
        pass

    def flushInput(self):
        self.__data = None

    def flushOutput(self):
        pass

    ## readline()
    # reads characters from the fake Arduino until a \n is found.
    def readline(self):
        print(self._data)
        try:
            returnIndex = self._data.index("\n")
        except ValueError:
            raise NoDataAvailableException()

        if returnIndex != -1:
            s = self._data[0:returnIndex + 1]
            self._data = self._data[returnIndex + 1:]
            return s
        else:
            return ""

    ## __str__()
    # returns a string representation of the serial class
    def __str__(self):
        return "Serial<id=0xa81c10, open=%s>( port='%s', baudrate=%d," \
               % (str(self.isOpen), self.port, self.baudrate) \
               + " bytesize=%d, parity='%s', stopbits=%d, xonxoff=%d, rtscts=%d)" \
               % (self.bytesize, self.parity, self.stopbits, self.xonxoff,
                  self.rtscts)
