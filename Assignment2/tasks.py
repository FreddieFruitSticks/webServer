import os, json
from email.utils import formatdate
from ResponseBuilder import ResponseBuilder, build_generic_response


# Each task must close it's own connection

# handles HEAD request too since HEAD = GET without a body
def task_handle_get(connection, file_name, user_agent, head_request):
    response_builder = ResponseBuilder()
    response_builder.with_date(formatdate(timeval=None, localtime=False, usegmt=True)) \
        .with_content_type("text/html; charset=utf-8") \
        .with_server("FredServer") \
        .with_user_agent(user_agent)

    try:
        file_path = os.getcwd() + "/text_files/" + file_name
        my_file = open(file_path)
        if not head_request:
            l = my_file.read(1024)
        else:
            l = None
        response_builder.with_body(l) \
            .with_status(200) \
            .with_content_length(os.path.getsize(file_path)) \
            .with_status_en("OK")
        connection.send(response_builder.build())
        while l and not head_request:
            l = my_file.read(1024)
            connection.send(l)
        my_file.close()
    except IOError:
        l = """
<html><body><h1>File Not Found</h1></body></html>
"""
        response_builder.with_body(l) \
            .with_status(404) \
            .with_status_en("File Not Found") \
            .with_content_length(0)

        connection.send(response_builder.build())
    finally:
        connection.close()


def task_handle_post_request(connection, message_body, headers):
    expect_value = ''
    content_type = ''
    try:
        expect_value = headers['Expect']
        content_type = headers['Content-Type']
    except KeyError as e:
        print 'Expect header does not exist', e
    if expect_value == '100-continue':
        if content_type == 'application/json' and headers['protocol_version'] == '1.1':
            response = build_generic_response(100, "Continue", None).build()
            try:
                connection.send(response)
            except Exception as e:
                print e

        else:
            response = build_generic_response(417, "Expectation Failed", None).build()
    else:
        message = do_something_post(message_body)
        response = build_generic_response(200, "OK", None).with_body(message) \
            .with_content_length(len(message) + 1) \
            .build()
    try:
        connection.send(response)
    except Exception as e:
        print e
    finally:
        connection.close()


def task_handle_put_request(connection, message_body, headers):
    if 'Content-MD5' in headers:
        response = build_generic_response(501, "Not Implemented", None).build()
    elif 'Content-Length' not in headers or len(message_body) != headers.get('Content-Length'):
        response = build_generic_response(400, "Bad Request", None).build()
    elif 'Content-Type' not in headers:
        response = build_generic_response(400, "Bad Request", None).build()
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
        file_path = os.getcwd() + "/text_files/" + headers['file_name']
        if os.path.exists(file_path):
            os.remove(file_path)
            response = build_generic_response(200, "OK", None).build()
        else:
            response = build_generic_response(404, "Not Found", None).build()
    else:
        response = build_generic_response(400, "Bad Request", None).build()

    return response


def do_something_get():
    pass


def do_something_post(message_body):
    return message_body


def do_something_put(message_body, headers):
    file_path = os.getcwd() + "/text_files/" + headers['file_name']
    if os.path.exists(file_path):
        my_file = open(file_path, 'w')
        if len(message_body) > 0:
            my_file.write(message_body)
            response = build_generic_response(200, "OK", None).build()
        else:
            response = build_generic_response(204, "No Content", None).build()
    else:
        my_file = open(file_path, 'w+')
        my_file.write(message_body)
        response = build_generic_response(201, "Created", None).build()

    return response


def handle_expect_header():
    pass
