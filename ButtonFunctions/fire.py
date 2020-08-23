def ignition(application):
    application.connection.write("sup\r\n")


def supress(application):
    application.connection.write("fire\r\n")
