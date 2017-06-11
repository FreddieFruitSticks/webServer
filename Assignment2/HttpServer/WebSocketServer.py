from Utils import message_len_as_hex


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
            payload_byte = ''
            print "waiting for websocket message"
            payload_byte = connection.recv(1024)
            if len(payload_byte) != 0:
                while len(payload_byte) == 1024:
                    payload = payload + payload_byte
                    payload_byte = connection.recv(1024)

                print "payload_byte", payload_byte
                data_type = ord(payload_byte[0])
                mask_and_length = ord(payload_byte[1])
                length = mask_and_length & 127
                print "length",length
                if length <= 125:
                    mask = payload_byte[2:6]
                    print "mask", mask
                    print "len mask", len(mask)

                    masked_message = payload_byte[6:]
                    print "masked_message",masked_message
                    for ind, obj in enumerate(masked_message):
                        print ind,obj
                    message = [(ord(byte.encode('hex').decode('hex')) ^ ord(mask[index%4])) for index, byte in enumerate(masked_message)]
                    print "message", message
            else:
                print "connection closed on other side!"
                connection.close()
                closed = True
    except Exception:
        print "Exception in recv web sock message"
        raise
