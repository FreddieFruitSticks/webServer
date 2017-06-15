def message_len_as_hex(message_length):
    if message_length == 0 or message_length is None:
        return "00".decode('hex')
    hex_map = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    hex_base = 16
    quotient = message_length
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


# starting position is the beginning of the mask which is 4 bytes, rest is payload - is this method doing to much?
def recvall(connection, buff_size):
    data = ''
    length = 0
    starting_position = 0
    while len(data) < 2:
        data = data.join(connection.recv(buff_size))
    payload_length = ord(data[1]) & 127
    if payload_length <= 125:
        starting_position = 2
        length = payload_length
        while len(data[3:]) < length + 4:
            data = data.join(connection.recv(buff_size))
    elif payload_length == 126:
        while len(data) < 4:
            data = data.join(connection.recv(buff_size))
        starting_position = 4
        length = get_payload_length(data, 8)
        while len(data[4:]) < length + 4:
            data = data.join(connection.recv(buff_size))
    elif payload_length == 127:
        while len(data) < 10:
            data = data.join(connection.recv(buff_size))
        starting_position = 10
        length = get_payload_length(data, 8)
        while len(data[10:]) < length + 4:
            data = data.join(connection.recv(buff_size))

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
