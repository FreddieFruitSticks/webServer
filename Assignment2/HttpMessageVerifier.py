from NetworkExceptions import BadRequestException

supported_operations = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']


def verify_message(message):
    request_header = message.split('\n')[0]
    request_header_operation = request_header.split(" ")[0]
    request_header_protocol = request_header.split(" ")[2]
    protocol_version = request_header_protocol.split("/")[1]
    protocol_name = request_header_protocol.split("/")[0]

    if request_header_operation in supported_operations and protocol_name == 'HTTP'\
            and protocol_version.rstrip() == '1.1':
        print "operation is allowed", request_header_operation
    else:
        print "bad request - message not verified"
        raise BadRequestException("Bad Request. "+request_header)

