from NetworkExceptions import BadRequestException, HttpVersionException

supported_operations = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']


def parse_headers(message):
    message_split = message.split('\r\n')
    headers_as_dict = parse_headers_to_dict(message_split)

    request_header = message_split[0]
    request_header_split = request_header.split(" ")

    request_header_operation = request_header_split[0]
    if len(request_header_split) == 3:
        request_header_protocol = request_header_split[2]
        headers_as_dict['file_name'] = request_header_split[1].split("/")[1]
    else:
        request_header_protocol = request_header_split[1]

    protocol_name = request_header_protocol.split("/")[0]
    protocol_version = request_header_protocol.split("/")[1].rstrip()
    headers_as_dict['request_operation'] = request_header_split[0]
    headers_as_dict['protocol_version'] = protocol_version

    if request_header_operation in supported_operations and protocol_name == 'HTTP' \
            and protocol_version == '1.1' and 'Host' in headers_as_dict:
        return headers_as_dict
    elif protocol_version != '1.1':
        raise HttpVersionException("HTTP Version Not Supported")
    else:
        print "operation not allowed", request_header_operation
        raise BadRequestException("Bad Request. " + request_header)


def parse_headers_to_dict(message_split):
    dict = {}
    for header in message_split[1:len(message_split) - 2]:
        split_up = header.split(": ")
        dict[split_up[0]] = split_up[1]
    return dict
