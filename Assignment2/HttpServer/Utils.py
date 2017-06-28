from NetworkExceptions import ConnectionAbruptlyClosedException
import re, base64


def int_as_hex(integer):
    if integer == 0 or integer is None:
        return "00".decode('hex')
    hex_map = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    hex_base = 16
    quotient = integer
    my_list = []

    while quotient != 0:
        next_quotient = quotient / hex_base
        rem = quotient % hex_base
        quotient = next_quotient
        if rem < 10:
            my_list.append(str(rem))
        else:
            my_list.append(hex_map.get(rem))

        if quotient == 0:
            rem = quotient % hex_base
            if rem < 10:
                my_list.append(str(rem))
            else:
                my_list.append(hex_map.get(rem))
    hex_val = reduce(lambda x, y: x + y, reversed(my_list))
    if len(hex_val) % 2 != 0:
        hex_val = hex_val[1:]
    return hex_val.decode('hex')


def verify_websocket_handshake(headers):
    pattern = re.compile(
        '^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$')  # regex to verify b64 encoded
    isB64 = pattern.match(headers.get("Sec-WebSocket-Key"))
    if isB64 is not None:
        decoded = base64.b64decode(headers.get("Sec-WebSocket-Key"));
        if len(decoded) != 16:
            isB64 = None

    if headers.get("Upgrade").lower() == "websocket" and \
                    isB64 is not None and \
                    headers.get("Sec-WebSocket-Version") == "13" and \
                    headers.get("Host") is not None:
        return True
    return False


# starting position is the beginning of the mask which is 4 bytes, rest is payload - is this method doing to much?
def recvall_websocket(connection, buff_size):
    data = ''
    length = 0
    starting_position = 0
    while len(data) < 2:
        recv = connection.recv(buff_size)
        if not recv: raise ConnectionAbruptlyClosedException
        data = data + recv
    payload_length = ord(data[1]) & 127
    if payload_length <= 125:
        starting_position = 2
        length = payload_length
        while len(data[starting_position:]) < length + 4:
            recv = connection.recv(buff_size)
            data = data + recv
    elif payload_length == 126:
        while len(data) < 4:
            recv = connection.recv(buff_size)
            data = data + recv
        starting_position = 4
        length = get_payload_length(data, 2)  # following two bits represent the length of payload
        while len(data[starting_position:]) < length + 4:
            recv = connection.recv(buff_size)
            data = data + recv
    elif payload_length == 127:
        while len(data) < 10:
            recv = connection.recv(buff_size)
            data = data + recv
        starting_position = 10
        length = get_payload_length(data, 8)  # following eight bits represent the length of payload
        while len(data[starting_position:]) < length + 4:
            recv = connection.recv(buff_size)
            data = data + recv

    return data, length, starting_position


def get_payload_length(data, number_of_bits):
    if number_of_bits not in (1, 2, 8):
        return None
    length = 0
    i = 0
    while number_of_bits > 0:
        length += ord(data[2 + i]) << 8 * (number_of_bits - 1)
        i += 1
        number_of_bits -= 1
    return length


# this is by NO means a receive all. Deal with this properly (when i have time!)
def recvall_http(connection, buff_size):
    full_message = ''
    message_portion = connection.recv(buff_size)
    full_message = full_message + message_portion
    return full_message
