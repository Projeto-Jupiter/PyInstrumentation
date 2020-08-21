from main import connection


def ignition():
    connection.write("sup\r\n")


def supress():
    connection.write("fire\r\n")
