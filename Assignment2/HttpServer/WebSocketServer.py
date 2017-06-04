def send_web_sock_message(connection, message):
    payload = []
    payload.insert(0, '\x81')  # indicates text

    if len(message) <= 125:
        payload.insert(1, '\x01')

    payload.insert(2, '\x70')
    for frame in payload:
        print frame
        connection.send(frame)


def recv_web_sock_message(connection):
    repeat = True
    while repeat:
        try:
            fullMessage = ''
            message = connection.recv(1024)
            while len(message) == 1024:
                fullMessage += message
                message = connection.recv(1024)
            fullMessage += message
            print message
            repeat = False
        except KeyboardInterrupt:
            raise
