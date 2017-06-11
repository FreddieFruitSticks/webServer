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
