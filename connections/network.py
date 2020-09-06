class ConnectionNotFoundException(Exception):
    pass


class NetworkConfigurator:

    def __init__(self, configurations_data, connection_module, handler):
        self.configuration = configurations_data
        self.connection_module = connection_module
        self.connection_handler = handler
        self.connections = []
        self._set_up_connection()
        print(self.connections)

    def _set_up_connection(self):
        for connection in self.configuration:
            name, connection_type = connection.pop('name'), connection.pop('type')
            connection_handler = self.connection_handler(module=self.connection_module, **connection)
            self.connections.append({'name': name,
                                     'type': connection_type,
                                     'handler': connection_handler})

    def get_handler(self, name):
        for connection in self.connections:
            print(f'o valor e {connection}')
            if connection['name'] == name:
                return connection['handler']
        message = f'Connection {name} not found'
        print(message)
        raise (ConnectionNotFoundException(f'Connection {name} not found'))
