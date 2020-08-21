def fire(connection, flag):
    if flag:  # Supress command
        on = False
        connection.write("sup\r\n")
    else:  # Fire command
        on = True
        connection.write("fire\r\n")
    return on
