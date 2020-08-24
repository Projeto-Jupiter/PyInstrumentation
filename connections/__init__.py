from abc import ABC, abstractmethod


class NoDataAvailableException(Exception):
    """Exception to be raised when there isn't any data available for retrieval"""
    pass


class ConnectionHandler(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def flush_buffer(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass
