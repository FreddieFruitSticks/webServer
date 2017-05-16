import os, json, sys
from email.utils import formatdate
from ResponseBuilder import ResponseBuilder, build_generic_response
# from HttpMessageVerifier import parse_headers_to_dict
from ContextManagers import CaptureOutput

sys.path.insert(0, '/home/freddie/IdeaProjects/networking/Assignment2/app')
sys.path.insert(0, '/home/freddie/IdeaProjects/networking/Assignment2/CGI')
from run_with_wsgi import run_with_wsgi
from simple_app import simple_app


# Each task must close it's own connection

# handles HEAD request too since HEAD = GET without a body
def task_handle_get(connection, headers, head_request):
    try:
        # do_something_get(connection, headers, head_request)
        do_something_get(connection, headers, head_request)
    except KeyError as e:
        print e


def task_handle_post_request(connection, message_body, headers):
    response = do_something_post(message_body, headers)
    try:
        connection.send(response)
    except Exception as e:
        print e
    finally:
        connection.close()


# TODO: IF-MATCH etags page 129
def task_handle_put_request(connection, message_body, headers):
    if 'Content-MD5' in headers:
        response = build_generic_response(501, "Not Implemented")
    elif 'Content-Length' not in headers or len(message_body) != int(headers.get('Content-Length')):
        response = build_generic_response(400, "Bad Request")
    elif 'Content-Type' not in headers:
        response = build_generic_response(400, "Bad Request")
    else:
        response = do_something_put(message_body, headers)
    try:
        connection.send(response)
    except Exception as e:
        print e
    finally:
        connection.close()


def task_handle_delete_request(connection, headers):
    response = do_something_delete(headers)
    try:
        connection.send(response)
    except Exception as e:
        print e
    finally:
        connection.close()


# TODO: Move these in to another file - this is where the WSGI API will be handled
def do_something_delete(headers):
    if 'file_name' in headers:
        file_path = os.getcwd() + "/../text_files/" + headers['file_name']
        permissions = os.stat(file_path)
        permission = int(oct(permissions.st_mode)[-1:])
        if permission | 2 != permission:
            return build_generic_response(403, "Forbidden")
        if os.path.exists(file_path):
            os.remove(file_path)
            response = build_generic_response(200, "OK")
        else:
            response = build_generic_response(404, "Not Found")
    else:
        response = build_generic_response(400, "Bad Request")

    return response


# TODO: Need to change response builder to be able to dynamically add the output headers to the server response headers
def wsgi_get(connection, headers, head_request):
    print(headers)
    with CaptureOutput() as output:
        run_with_wsgi(simple_app)
    print output


def do_something_get(connection, headers, head_request):
    try:
        file_path = os.getcwd() + "/../text_files/" + headers['file_name']
        permissions = os.stat(file_path)
        permission = int(oct(permissions.st_mode)[-1:])
        if permission | 4 != permission:
            response = build_generic_response(403, "Forbidden")
            connection.send(response)
        else:
            my_file = open(file_path)

            if not head_request:
                body = my_file.read(1024)
            else:
                body = None
            response = ResponseBuilder(200, "OK")
            response = response.with_header({"key": "Date", "value": formatdate(timeval=None, localtime=False, usegmt=True)}) \
                .with_header({"key": "Content-type", "value": "text/html; charset=utf-8"}) \
                .with_header({"key": "Host", "value": "FredServer"}) \
                .with_header({"key": "Content-length", "value": os.path.getsize(file_path)}) \
                .with_body({"body": body}) \
                .build_response()

            connection.send(response)
            while body and not head_request:
                body = my_file.read(1024)
                connection.send(body)
            my_file.close()
    except IOError:
        body = """
<html><body><h1>File Not Found</h1></body></html>
"""
        response = ResponseBuilder(404, "File Not Found")
        response = response.with_header(
            {"key": "Date", "value": formatdate(timeval=None, localtime=False, usegmt=True)}) \
            .with_header({"key": "Content-type", "value": "text/html; charset=utf-8"}) \
            .with_header({"key": "Host", "value": "FredServer"}) \
            .with_header({"key": "Content-length", "value": 0}) \
            .with_body({"body": body}) \
            .build_response()
        connection.send(response)
    finally:
        connection.close()


def do_something_post(message_body, headers):
    expect_value = ''
    content_type = ''
    try:
        expect_value = headers['Expect']
        content_type = headers['Content-Type']
    except KeyError as e:
        print 'Header does not exist', e
    if expect_value == '100-continue':
        if content_type == 'application/json' and headers['protocol_version'] == '1.1':
            response = build_generic_response(100, "Continue")
        else:
            response = build_generic_response(417, "Expectation Failed")
    else:
        message_len = len(message_body) + 1
        response = ResponseBuilder(200, "OK")
        response = response.with_header({"key": "Date", "value": formatdate(timeval=None, localtime=False, usegmt=True)}) \
            .with_header({"key": "Content-type", "value": "text/html; charset=utf-8"}) \
            .with_header({"key": "Host", "value": "FredServer"}) \
            .with_header({"key": "Content-length", "value": message_len})\
            .with_body({"body": message_body})\
            .build_response()
    return response


def do_something_put(message_body, headers):
    file_path = os.getcwd() + "/../text_files/" + headers['file_name']

    if os.path.exists(file_path):
        permissions = os.stat(file_path)
        permission = int(oct(permissions.st_mode)[-1:])
        if permission | 2 != permission:
            return build_generic_response(403, "Forbidden")
        my_file = open(file_path, 'w')
        if len(message_body) > 0:
            my_file.write(message_body)
            response = build_generic_response(200, "OK")
        else:
            response = build_generic_response(204, "No Content")
        my_file.close()
    else:
        my_file = open(file_path, 'w+')
        os.chmod(file_path, 0o646)
        my_file.write(message_body)
        response = build_generic_response(201, "Created")
        my_file.close()

    return response
