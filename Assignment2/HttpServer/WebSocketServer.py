from Utils import message_len_as_hex


def send_close_frame(connection, reason):
    payload = []
    payload.insert(0, '\x81')
    message_length = 2
    payload.insert(1, message_len_as_hex(message_length))
    payload.insert(2, message_len_as_hex((reason >> 8) & 255))
    payload.insert(3, message_len_as_hex(reason & 255))

    map(lambda frame: connection.sendall(frame), payload)


def send_web_sock_message(connection, message):
    payload = []
    payload.insert(0, '\x81')  # 1000 0001 -> first 1 for FIN, 3 0's for RSV's and 0001 (0x01) for text
    message_length = len(message)

    if len(message) <= 125:
        payload.insert(1, message_len_as_hex(message_length))
        payload.insert(2, message)
    elif 125 < len(message) <= 65535:
        payload.insert(1, message_len_as_hex(126))
        payload.insert(2, message_len_as_hex((message_length >> 8) & 255))
        payload.insert(3, message_len_as_hex(message_length & 255))
        payload.insert(4, message)
    elif len(message) > 65535:
        payload.insert(1, message_len_as_hex(127))
        payload.insert(2, message_len_as_hex((message_length >> 56) & 255))
        payload.insert(3, message_len_as_hex((message_length >> 48) & 255))
        payload.insert(4, message_len_as_hex((message_length >> 40) & 255))
        payload.insert(5, message_len_as_hex((message_length >> 32) & 255))
        payload.insert(6, message_len_as_hex((message_length >> 24) & 255))
        payload.insert(7, message_len_as_hex((message_length >> 16) & 255))
        payload.insert(8, message_len_as_hex((message_length >> 8) & 255))
        payload.insert(9, message_len_as_hex(message_length & 255))
        payload.insert(10, message)

    map(lambda frame: connection.sendall(frame), payload)


def recv_web_sock_message(connection):
    closed = False
    try:
        while not closed:
            payload = ''
            print "waiting for websocket message"
            payload_byte = connection.recv(1024)
            if len(payload_byte) != 0:
                while len(payload_byte) == 1024:
                    payload = payload + payload_byte
                    payload_byte = connection.recv(1024)

                data_type = ord(payload_byte[0])
                mask_bit_and_length = ord(payload_byte[1])

                length = mask_bit_and_length & 127
                if length <= 125:
                    mask = payload_byte[2:6]
                    masked_message = payload_byte[6:length + 7]
                    if data_type == 136:
                        print "!!CLOSING!!!"
                        closed = True
                        message = [ord(byte) ^ ord(mask[index % 4]) for index, byte in
                                   enumerate(masked_message)]
                        first_byte = message[0] << 8
                        second_byte = message[1]
                        shutdown_reason = first_byte + second_byte
                        send_close_frame(connection, shutdown_reason)
                        connection.close()
                    else:
                        message = [chr(ord(byte) ^ ord(mask[index % 4])) for index, byte in
                                   enumerate(masked_message)]
                        # send_close_frame(connection, 1000)
                        # closed = True

                    print "message", message
                elif length == 126:
                    first_byte = ord(payload_byte[2]) << 8
                    second_byte = ord(payload_byte[3])
                    mask = payload_byte[4:8]
                    payload_length = first_byte + second_byte
                    masked_message = payload_byte[8:payload_length + 9]
                    message = [chr(ord(byte) ^ ord(mask[index % 4])) for index, byte in enumerate(masked_message)]
                    print message
                elif length == 127:
                    first_byte = ord(payload_byte[2]) << 56
                    second_byte = ord(payload_byte[3]) << 48
                    third_byte = ord(payload_byte[4]) << 40
                    fourth_byte = ord(payload_byte[5]) << 32
                    fifth_byte = ord(payload_byte[6]) << 24
                    sixth_byte = ord(payload_byte[7]) << 16
                    seventh_byte = ord(payload_byte[8]) << 8
                    eighth_byte = ord(payload_byte[9])
                    mask = payload_byte[10:14]
                    payload_length = first_byte + second_byte + third_byte + fourth_byte + fifth_byte + sixth_byte + seventh_byte + eighth_byte
                    masked_message = payload_byte[14:payload_length + 15]
                    message = [chr(ord(byte) ^ ord(mask[index % 4])) for index, byte in enumerate(masked_message)]
                    print message
            else:
                print "connection closed on other side!"
                shutdown_reason = 1000
                send_close_frame(connection, shutdown_reason)
                connection.close()
                closed = True
    except Exception:
        print "Exception in recv web sock message"
        raise
