from NetworkExceptions import BadRequestException

supported_operations = ['GET', 'POST', 'PUT', 'DELETE']


def verify_message(message):
    request_header = message.split('\n')[0]
    request_header_operation = request_header.split(" ")[0]

    if request_header_operation in supported_operations:
        print "operation is allowed", request_header_operation
    else:
        raise BadRequestException(request_header_operation + " not a supported operation")

