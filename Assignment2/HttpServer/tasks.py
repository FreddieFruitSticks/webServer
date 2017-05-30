from FileServerTasks import *
from WebServerTasks import *


# Each task must close it's own connection

# handles HEAD request too since HEAD = GET without a body
def set_wsgi_env(headers, query_params, server_env):
    if headers.get('Content-length') is not None:
        server_env.set_env_var('CONTENT_LENGTH', headers.get('Content-length'))
    server_env.set_env_var('HTTP_ACCEPT', headers.get('Content-Type'))
    server_env.set_env_var('HTTP_USER_AGENT', headers.get('User-Agent'))
    server_env.set_env_var('QUERY_STRING', query_params)
    server_env.set_env_var('REQUEST_METHOD', headers.get('request_operation'))
    server_env.set_env_var('SCRIPT_NAME', '')
    server_env.set_env_var('PATH_INFO', headers.get('file_name'))


def task_handle_get(connection, headers, head_request, server_env, query_params):
    set_wsgi_env(headers, query_params, server_env)

    try:
        wsgi_get(connection, headers, head_request, server_env)
        # do_something_get(connection, headers, head_request)
    except KeyError as e:
        print e


def task_handle_post_request(connection, message_body, headers, query_params, server_env):
    set_wsgi_env(headers, query_params, server_env)
    response = do_something_post(message_body, headers)
    try:
        connection.send(response)
    except Exception as e:
        print e
    finally:
        connection.close()


# TODO: IF-MATCH etags page 129
def task_handle_put_request(connection, message_body, headers, query_params, server_env):
    if 'Content-MD5' in headers:
        response = build_generic_response(501, "Not Implemented")
    elif 'Content-Length' not in headers or len(message_body) != int(headers.get('Content-Length')):
        response = build_generic_response(400, "Bad Request")
    elif 'Content-Type' not in headers:
        response = build_generic_response(400, "Bad Request")
    else:
        set_wsgi_env(headers, query_params, server_env)
        response = do_something_put(message_body, headers)
    try:
        connection.send(response)
    except Exception as e:
        print e
    finally:
        connection.close()


def task_handle_delete_request(connection, headers, query_params, server_env):
    set_wsgi_env(headers, query_params, server_env)
    response = do_something_delete(headers)
    try:
        connection.send(response)
    except Exception as e:
        print e
    finally:
        connection.close()
