from NetworkExceptions import BadRequestException, HttpVersionException
import os, stat

supported_operations = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']


def parse_headers(message):
    message_split = message.split('\r\n')
    headers_as_dict = parse_headers_to_dict(message_split)
    request_header = message_split[0]
    request_header_split = request_header.split(" ")

    request_header_operation = request_header_split[0]
    protocol_name, protocol_version, query_params = parse_request_line(headers_as_dict, request_header_split)
    verify_access_permissions(headers_as_dict)
    if request_header_operation in supported_operations and protocol_name == 'HTTP' \
            and protocol_version == '1.1' and 'Host' in headers_as_dict:
        return headers_as_dict, query_params
    elif protocol_version != '1.1':
        raise HttpVersionException("HTTP Version Not Supported")
    else:
        print "operation not allowed", request_header_operation
        raise BadRequestException("Bad Request. " + request_header)


def verify_access_permissions(headers):
    if ".." in headers.get("file_name"):
        raise BadRequestException("Bad Request")


def parse_request_line(headers_as_dict, request_header_split):
    query_params = None
    if len(request_header_split) == 3:
        request_header_protocol = request_header_split[2]
        if "?" in request_header_split[1]:
            headers_as_dict['file_name'], query_params = get_query_params(request_header_split[1])
        else:
            headers_as_dict['file_name'] = request_header_split[1]
    else:
        request_header_protocol = request_header_split[1]

    protocol_name = request_header_protocol.split("/")[0]
    protocol_version = request_header_protocol.split("/")[1].rstrip()
    headers_as_dict['request_operation'] = request_header_split[0]
    headers_as_dict['protocol_version'] = protocol_version
    return protocol_name, protocol_version, query_params


def get_query_params(request_line):
    if request_line is None:
        return None

    query_params = {}
    query_params_string = request_line.split("?")
    if len(query_params_string) > 2:
        raise BadRequestException("Bad Request")
    params_array = query_params_string[1].split("&")
    for kwargs_params in params_array:
        key_value = kwargs_params.split("=")
        query_params[key_value[0]] = key_value[1]
    return query_params_string[0], query_params


def parse_headers_to_dict(message_split):
    dict = {}
    for header in message_split[1:len(message_split) - 2]:
        split_up = header.split(": ")
        dict[split_up[0]] = split_up[1]
    return dict
